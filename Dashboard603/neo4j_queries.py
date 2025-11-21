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
    query = """
    MATCH (t:Tag)
    RETURN t.name AS tag
    ORDER BY tag
    """
    return list(tx.run(query))


def get_all_book_titles(tx, limit=1000):
    """Get list of book titles for dropdowns, sorted by popularity."""
    query = """
    MATCH (b:Book)
    RETURN b.title AS title
    ORDER BY b.ratings_count DESC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


def get_books_by_tag(tx, tag, min_avg_rating):
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


def get_recommendation_graph_data(tx, title, limit=40):
    """
    Data for visualization: main book, tags, other books sharing those tags.
    """
    query = """
    MATCH (b:Book {title:$title})-[:TAGGED_AS]->(t:Tag)<-[:TAGGED_AS]-(other:Book)
    WHERE other <> b
    RETURN b.title AS main_book,
           t.name AS tag,
           other.title AS recommended_book
    LIMIT $limit
    """
    return list(tx.run(query, title=title, limit=limit))


# ---------------------------------------------------------
# 2. Shortest Path – cleaned output
# ---------------------------------------------------------
def get_shortest_path(tx, title1, title2):
    """
    Returns a single record with:
      path_nodes: [ "Book A", "Tag: dystopian", "Book B" ]
      hops:       number of relationships in the path
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
    query = """
    MATCH (a:Author)-[:WRITTEN_BY]-(b:Book)
    RETURN a.name AS author,
           COUNT(b) AS books_written
    ORDER BY books_written DESC, author ASC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


def get_authors_by_tag(tx, tag_name, limit=50):
    """Get authors who write books with a specific tag/genre."""
    query = """
    MATCH (a:Author)-[:WRITTEN_BY]-(b:Book)-[:TAGGED_AS]->(t:Tag)
    WHERE toLower(t.name) = toLower($tag)
    WITH a.name AS author, COUNT(DISTINCT b) AS books_written, 
         AVG(b.average_rating) AS avg_rating
    RETURN author, books_written, ROUND(avg_rating, 2) AS avg_rating
    ORDER BY books_written DESC, avg_rating DESC
    LIMIT $limit
    """
    return list(tx.run(query, tag=tag_name, limit=limit))


def get_top_tags(tx, limit):
    query = """
    MATCH (t:Tag)<-[:TAGGED_AS]-(b:Book)
    RETURN t.name AS tag,
           COUNT(b) AS book_count
    ORDER BY book_count DESC, tag ASC
    LIMIT $limit
    """
    return list(tx.run(query, limit=limit))


# ---------------------------------------------------------
# 4. Traversal – related books by tags and authors
# ---------------------------------------------------------
def get_related_books_by_tags(tx, title):
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
