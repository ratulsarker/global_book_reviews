from neo4j import GraphDatabase

# ---------------------------------------------------------
# Neo4j connection
# ---------------------------------------------------------
# 🔧 Change these to match your Neo4j instance (or use env vars if you want)
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "adminadmin"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
    database="goodbooks-2025-11-20t18-16-45"
)


# ---------------------------------------------------------
# 1. Basic tag + book queries for main dashboard
# ---------------------------------------------------------
def get_all_tags(tx):
    """
    Get all meaningful tags (filters out junk tags like numbers, ratings, years).
    
    Dashboard Locations:
    - Graph Database Insights > Book Discovery & Recommendations tab > Browse High-Rated Books by Genre/Tag (tag selector dropdown)
    - Graph Database Insights > Advanced Graph Algorithms tab > Author Influence Analysis (genre filter dropdown)
    """
    query = """
    MATCH (t:Tag)<-[:TAGGED_AS]-(b:Book)
    WHERE t.name IS NOT NULL 
      AND t.name <> ''
      AND NOT t.name =~ '^[0-9].*'
      AND NOT t.name =~ '.*[0-9]{4}.*'
      AND NOT t.name =~ '.*-star.*'
      AND NOT t.name =~ '.*star$'
      AND NOT t.name IN ['-', '--', '---', '1', '2', '3', 'mine', 'own', 'owned', 'have', 'default']
      AND NOT t.name STARTS WITH 'read-'
      AND NOT t.name STARTS WITH 'to-'
      AND NOT t.name STARTS WITH 'my-'
      AND size(t.name) > 2
    WITH t.name AS tag, COUNT(b) AS book_count
    WHERE book_count >= 10
    RETURN tag
    ORDER BY tag
    """
    return list(tx.run(query))


def get_all_book_titles(tx, limit=1000):
    """
    Get list of book titles for dropdowns, sorted by popularity.
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab
    Used to populate book selection dropdowns in:
    - Shortest Path Analysis (Starting Book and Destination Book selectors)
    - Book Relationship Explorer (Select Book to Explore dropdown)
    """
    query = """
    MATCH (b:Book)
    RETURN b.title AS title
    ORDER BY b.ratings_count DESC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


def get_books_by_tag(tx, tag, min_avg_rating):
    """
    Get books filtered by tag/genre with minimum rating threshold.
    
    Dashboard Location: Graph Database Insights > Book Discovery & Recommendations tab > Browse High-Rated Books by Genre/Tag
    Displays a dataframe of books matching the selected tag and minimum rating filter.
    """
    query = """
    MATCH (b:Book)-[:TAGGED_AS]->(t:Tag)
    WHERE toLower(t.name) = toLower($tag)
      AND b.average_rating >= $min_rating
    RETURN b.title AS title,
           b.average_rating AS average_rating,
           b.ratings_count AS ratings_count
    ORDER BY average_rating DESC, ratings_count DESC
    LIMIT 50
    """
    return list(tx.run(query, tag=tag, min_rating=min_avg_rating))


def search_books_by_keyword(tx, keyword, limit=30):
    """
    Search for books by title keyword.
    
    Dashboard Location: Graph Database Insights > Book Discovery & Recommendations tab > Personalized Book Recommendations
    Used in the book search functionality to find books by title, which then populates the book selection dropdown.
    """
    query = """
    MATCH (b:Book)
    WHERE toLower(b.title) CONTAINS toLower($keyword)
    RETURN b.title AS title,
           b.average_rating AS average_rating
    ORDER BY average_rating DESC
    LIMIT $limit
    """
    return list(tx.run(query, keyword=keyword, limit=limit))


def get_recommendations_for_book(tx, title, limit=30):
    """
    Simple graph-based recommendation:
    Books that share tags with the selected book.
    
    Dashboard Location: Graph Database Insights > Book Discovery & Recommendations tab > Recommended Books Based on Shared Tags
    Displays a dataframe showing similar books that share common tags with the selected book, sorted by number of shared tags.
    """
    query = """
    MATCH (b:Book {title:$title})-[:TAGGED_AS]->(t:Tag)<-[:TAGGED_AS]-(other:Book)
    WHERE other <> b
    WITH other, count(t) AS shared_tags
    RETURN other.title AS recommended_title,
           shared_tags
    ORDER BY shared_tags DESC, recommended_title ASC
    LIMIT $limit
    """
    return list(tx.run(query, title=title, limit=limit))


def get_recommendation_graph_data(tx, title, num_books=10, min_rating=3.5):
    """
    Data for visualization: Shows multiple books and how they interconnect through tags.
    Returns a richer network showing book communities.
    
    Dashboard Location: Graph Database Insights > Book Discovery & Recommendations tab > Book Recommendation Network
    Generates the data for the interactive network graph visualization showing:
    - Selected book (blue box) at center
    - Similar recommended books (green ellipses) in a circle
    - Shared tags (orange dots) connecting books
    The graph can be customized with sliders for number of books, minimum rating, and physics settings.
    """
    query = """
    // Get the main book and its tags
    MATCH (mainBook:Book {title:$title})-[:TAGGED_AS]->(mainTag:Tag)
    WHERE mainTag.name IS NOT NULL 
      AND NOT mainTag.name =~ '^[0-9-]+$'
      AND size(mainTag.name) > 2
    WITH mainBook, COLLECT(DISTINCT mainTag) AS mainTags
    
    // Find top recommended books that share these tags
    UNWIND mainTags AS t
    MATCH (t)<-[:TAGGED_AS]-(recBook:Book)
    WHERE recBook <> mainBook
      AND recBook.average_rating >= $min_rating
    WITH mainBook, mainTags, recBook, COUNT(DISTINCT t) AS shared_tags, recBook.average_rating AS rating
    ORDER BY shared_tags DESC, rating DESC
    LIMIT $num_books
    
    // Collect recommended books and ADD main book to the list
    WITH mainBook, mainTags, COLLECT(recBook) AS topBooks
    WITH mainBook, mainTags, topBooks + [mainBook] AS allBooks
    
    // Get all tag connections for all books (including main book)
    UNWIND allBooks AS book
    MATCH (book)-[:TAGGED_AS]->(t:Tag)
    WHERE t IN mainTags
    WITH mainBook, book, t,
         CASE WHEN book = mainBook THEN 1 ELSE 0 END AS is_main,
         book.average_rating AS rating
    RETURN mainBook.title AS main_book,
           book.title AS book_title,
           t.name AS tag,
           is_main,
           rating
    ORDER BY is_main DESC, rating DESC
    """
    return list(tx.run(query, title=title, num_books=num_books, min_rating=min_rating))


# ---------------------------------------------------------
# 2. Shortest Path – cleaned output
# ---------------------------------------------------------
def get_shortest_path(tx, title1, title2):
    """
    Returns a single record with:
      path_nodes: [ "Book A", "Tag: dystopian", "Book B" ]
      hops:       number of relationships in the path
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > Shortest Path Analysis
    Finds the shortest connection path between two books through tags, authors, or other books.
    Displays the path as a chain (e.g., "Book A → Tag: dystopian → Book B") and shows degrees of separation.
    """
    query = """
    MATCH (b1:Book {title:$title1}),
          (b2:Book {title:$title2})
    MATCH p = shortestPath((b1)-[*..6]-(b2))
    WITH p, nodes(p) AS ns
    RETURN [n IN ns |
              CASE
                WHEN 'Book' IN labels(n)   THEN n.title
                WHEN 'Tag' IN labels(n)    THEN 'Tag: ' + n.name
                WHEN 'Author' IN labels(n) THEN 'Author: ' + n.name
                ELSE 'Node'
              END
           ] AS path_nodes,
           length(p) AS hops
    """
    return list(tx.run(query, title1=title1, title2=title2))


# ---------------------------------------------------------
# 3. Centrality-style queries (simple degree centrality)
# ---------------------------------------------------------
def get_top_authors(tx, limit):
    """
    Get top authors by number of books written (degree centrality).
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > Author Influence Analysis
    When "All Genres" is selected, displays the most prolific authors sorted by number of books written.
    """
    query = """
    MATCH (a:Author)-[:WRITTEN_BY]-(b:Book)
    WITH a.name AS author,
         COUNT(b) AS books_written,
         ROUND(AVG(b.average_rating), 2) AS avg_rating
    RETURN author, books_written, avg_rating
    ORDER BY books_written DESC, author ASC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


def get_authors_by_tag(tx, tag_name, limit=50):
    """
    Get authors who write books with a specific tag/genre.
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > Author Influence Analysis
    When a specific genre/tag is selected in the filter, displays authors who write in that genre,
    sorted by number of books written and average rating.
    """
    query = """
    MATCH (a:Author)-[:WRITTEN_BY]-(b:Book)-[:TAGGED_AS]->(t:Tag)
    WHERE toLower(t.name) = toLower($tag)
    WITH a.name AS author,
         COUNT(DISTINCT b) AS books_written,
         AVG(b.average_rating) AS avg_rating
    RETURN author, books_written, ROUND(avg_rating, 2) AS avg_rating
    ORDER BY books_written DESC, avg_rating DESC
    LIMIT $limit
    """
    return list(tx.run(query, tag=tag_name, limit=limit))


def get_top_tags(tx, limit):
    """
    Get top tags, filtering out meaningless ones.
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > View Top Tags & Genres
    Displays the most popular tags/genres sorted by number of books associated with each tag.
    """
    query = """
    MATCH (t:Tag)<-[:TAGGED_AS]-(b:Book)
    WHERE t.name IS NOT NULL 
      AND t.name <> ''
      AND NOT t.name =~ '^[0-9-]+$'
      AND size(t.name) > 1
    RETURN t.name AS tag,
           COUNT(b) AS book_count
    ORDER BY book_count DESC, tag ASC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


def get_book_with_most_tags(tx):
    """
    Get the book(s) with the highest number of tags.
    
    Dashboard Location: Graph Database Insights > Key Insight banner (at the top of the page)
    Displays a prominent banner showing the book with the most tags, including its rating and author.
    This appears at the top of the Graph Database Insights page as a key statistic.
    """
    query = """
    MATCH (b:Book)-[:TAGGED_AS]->(t:Tag)
    WITH b, COUNT(t) AS tag_count
    ORDER BY tag_count DESC
    LIMIT 5
    RETURN b.title AS title,
           b.authors AS author,
           b.average_rating AS rating,
           tag_count
    """
    return list(tx.run(query))


# ---------------------------------------------------------
# 4. Traversal – related books by tags and authors
# ---------------------------------------------------------
def get_related_books_by_tags(tx, title):
    """
    Find books related to the selected book through shared tags.
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > Book Relationship Explorer > Find by Similar Tags
    Displays books that share tags with the selected book, showing which specific tags they share.
    """
    query = """
    MATCH (b:Book {title:$title})-[:TAGGED_AS]->(t:Tag)<-[:TAGGED_AS]-(other:Book)
    WHERE other <> b
    RETURN other.title AS title,
           t.name AS shared_tag
    ORDER BY shared_tag, title
    LIMIT 25
    """
    return list(tx.run(query, title=title))


def get_related_books_by_author(tx, title):
    """
    Find other books written by the same author as the selected book.
    
    Dashboard Location: Graph Database Insights > Advanced Graph Algorithms tab > Book Relationship Explorer > Find by Same Author
    Displays other works by the same author, sorted by average rating.
    """
    query = """
    MATCH (b:Book {title:$title})
    WITH b, b.authors AS author

    MATCH (other:Book)
    WHERE other.authors = author
      AND other.title <> b.title

    RETURN other.title AS title,
           other.average_rating AS rating,
           other.authors AS author
    ORDER BY rating DESC
    LIMIT 25;
    """
    return list(tx.run(query, title=title))
