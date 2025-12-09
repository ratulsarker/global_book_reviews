import streamlit as st
import pandas as pd
from neo4j_queries import (
    driver,
    get_all_tags,
    get_all_book_titles,
    get_books_by_tag,
    search_books_by_keyword,
    get_recommendations_for_book,
    get_recommendation_graph_data,
    get_shortest_path,
    get_top_authors,
    get_authors_by_tag,
    get_top_tags,
    get_related_books_by_tags,
    get_related_books_by_author,
)
import sql_queries as sql
from graph_utils import build_recommendation_graph
import streamlit.components.v1 as components

# Page config with custom theme
st.set_page_config(
    layout="wide",
    page_title="Goodbooks Dashboard",
    page_icon="📚",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional styling
st.markdown("""
<style>
    /* Clean header styling */
    h1 {
        font-family: 'Segoe UI', Tahoma, sans-serif;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #0068c9;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #0056a8;
        border: none;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 5px;
    }
    
    /* Metric cards - keep default Streamlit colors */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------
# Helper to run Neo4j read transactions
# ------------------------------
def run_neo4j_read(fn, *args, **kwargs):
    with driver.session() as session:
        return session.execute_read(fn, *args, **kwargs)


# ------------------------------
# Streamlit App
# ------------------------------
def main():
    st.title("📚 Goodbooks Analytics Platform")
    st.markdown("*Hybrid Database Architecture: Neo4j Graph Database & MySQL Relational Database*")

    st.sidebar.header("📊 Navigation")
    page = st.sidebar.radio("Select Analysis Type", ["Graph Database Insights", "SQL Database Analytics"])

    if page == "Graph Database Insights":
        neo4j_page()
    else:
        sql_page()


# ------------------------------
# NEO4J PAGE
# ------------------------------
def neo4j_page():
    st.header("🕸️ Graph Database Analysis")

    # Two subtabs: existing explorer + graph algorithms
    tab1, tab2 = st.tabs(["📚 Book Discovery & Recommendations", "🔬 Advanced Graph Algorithms"])

    # ============================================================
    # TAB 1 – YOUR EXISTING FEATURES
    # ============================================================
    with tab1:
        st.subheader("📖 Browse High-Rated Books by Genre/Tag")

        # Load tags
        tags = run_neo4j_read(get_all_tags)
        tag_list = [t["tag"] for t in tags]

        # Default to "action" if available
        default_idx = tag_list.index("action") if "action" in tag_list else 0

        selected_tag = st.selectbox("Select Genre/Tag", tag_list, index=default_idx)

        min_rating = st.slider("Minimum Average Rating", 3.0, 5.0, 4.5, 0.1)

        try:
            rows = run_neo4j_read(get_books_by_tag, selected_tag, min_rating)
            if rows:
                st.dataframe(pd.DataFrame(rows))
            else:
                st.info("No books found for this filter.")
        except Exception as e:
            st.error(f"Error querying Neo4j: {e}")

        st.markdown("---")

        # ============================================================
        # 2. BOOK SEARCH + SELECTION + TAG-BASED RECOMMENDATIONS
        # ============================================================
        st.subheader("🎯 Personalized Book Recommendations")

        # Prepare session state variables
        if "search_results" not in st.session_state:
            st.session_state.search_results = []

        if "selected_title" not in st.session_state:
            st.session_state.selected_title = None

        # Search bar
        keyword = st.text_input("Search for a Book by Title", "hunger games", placeholder="Enter book title or keyword...")

        if st.button("🔍 Search Books", use_container_width=True):
            st.session_state.search_results = run_neo4j_read(
                search_books_by_keyword, keyword
            )
            st.session_state.selected_title = None

        # Show dropdown only if results exist
        if st.session_state.search_results:
            titles = [m["title"] for m in st.session_state.search_results]

            selected = st.selectbox(
                "Select a Book from Results",
                titles,
                index=titles.index(st.session_state.selected_title)
                if st.session_state.selected_title in titles
                else 0,
            )

            # Save selected title
            st.session_state.selected_title = selected

            st.success(f"✓ **Selected Book:** {st.session_state.selected_title}")

            # Tag-based recommendations
            recs = run_neo4j_read(
                get_recommendations_for_book, st.session_state.selected_title
            )

            if recs:
                st.subheader("📚 Recommended Books Based on Shared Tags")
                st.dataframe(pd.DataFrame(recs), use_container_width=True)
            else:
                st.info("No recommendations available for this book.")

            # ============================================================
            # 3. RECOMMENDATION GRAPH VISUALIZATION
            # ============================================================
            st.subheader("🕸️ Book Community Network Visualization")

            # Graph controls
            st.markdown("**📊 Customize Your Network:**")
            graph_col1, graph_col2 = st.columns([2, 1])
            
            with graph_col1:
                num_similar_books = st.slider(
                    "Number of Similar Books to Show",
                    min_value=5,
                    max_value=20,
                    value=10,
                    step=1,
                    key="graph_num_books",
                    help="More books = richer network but potentially cluttered"
                )
            
            with graph_col2:
                min_book_rating = st.slider(
                    "Minimum Book Rating",
                    min_value=3.0,
                    max_value=4.8,
                    value=3.5,
                    step=0.1,
                    key="graph_min_rating",
                    help="Only show highly-rated similar books"
                )
            
            if st.button("🔄 Generate Network Graph", key="generate_graph_btn", use_container_width=True):
                graph_data = run_neo4j_read(
                    get_recommendation_graph_data, 
                    st.session_state.selected_title,
                    num_similar_books,
                    min_book_rating
                )

                if graph_data:
                    # Enhanced legend with stats
                    unique_books = len(set(r["book_title"] for r in graph_data))
                    unique_tags = len(set(r["tag"] for r in graph_data))
                    
                    st.success(f"✓ Network generated: {unique_books} books connected through {unique_tags} shared tags")
                    st.info("**Graph Legend:** 🔵 Blue Box = Your Selected Book | 🟣 Purple Dots = Shared Genres/Tags | 🟢 Green Ellipses = Similar Books\n\n**💡 Tips:** Hover over nodes for details | Larger nodes = more connections | Drag to rearrange | Scroll to zoom")
                    
                    net = build_recommendation_graph(graph_data)
                    if net:
                        net.save_graph("recommendations_graph.html")

                        with open("recommendations_graph.html", "r", encoding="utf-8") as f:
                            html_content = f.read()
                        
                        # Inject JavaScript to disable physics quickly - minimal movement
                        stabilization_script = """
                        <script>
                        (function() {
                            function disablePhysicsQuickly() {
                                try {
                                    // Find all script tags and look for network variable
                                    var scripts = document.querySelectorAll('script');
                                    for (var s of scripts) {
                                        var content = s.innerHTML || s.textContent || '';
                                        if (content.includes('new vis.Network')) {
                                            // Extract network variable name
                                            var match = content.match(/var\\s+(\\w+)\\s*=\\s*new\\s+vis\\.Network/);
                                            if (match) {
                                                var netVar = match[1];
                                                // Wait for network to be created
                                                var checkInterval = setInterval(function() {
                                                    try {
                                                        var network = eval(netVar);
                                                        if (network && typeof network.on === 'function') {
                                                            clearInterval(checkInterval);
                                                            // Disable physics immediately after stabilization starts
                                                            network.on("stabilizationStart", function() {
                                                                // Disable after just 1 second of stabilization
                                                                setTimeout(function() {
                                                                    try {
                                                                        network.setOptions({ physics: false });
                                                                    } catch(e) {}
                                                                }, 1000);
                                                            });
                                                            // Disable physics after stabilization completes
                                                            network.on("stabilizationEnd", function() {
                                                                network.setOptions({ physics: false });
                                                            });
                                                            // Backup: disable after 2 seconds regardless
                                                            setTimeout(function() {
                                                                try {
                                                                    network.setOptions({ physics: false });
                                                                } catch(e) {}
                                                            }, 2000);
                                                        }
                                                    } catch(e) {
                                                        // Variable not ready yet
                                                    }
                                                }, 50);
                                                setTimeout(function() { clearInterval(checkInterval); }, 3000);
                                                break;
                                            }
                                        }
                                    }
                                } catch(e) {
                                    console.log('Physics disable script error:', e);
                                }
                            }
                            if (document.readyState === 'loading') {
                                document.addEventListener('DOMContentLoaded', disablePhysicsQuickly);
                            } else {
                                setTimeout(disablePhysicsQuickly, 200);
                            }
                        })();
                        </script>
                        """
                        # Insert script before closing body tag
                        html_content = html_content.replace('</body>', stabilization_script + '</body>')

                        components.html(html_content, height=770, scrolling=False)
                    else:
                        st.warning("Graph generation failed - insufficient data")
                else:
                    st.info("Insufficient data to generate network visualization. Try lowering the minimum rating.")
        else:
            st.info("💡 **Get Started:** Search for a book above to view personalized recommendations and network visualization.")

    # ============================================================
    # TAB 2 – GRAPH ALGORITHMS (NEW)
    # ============================================================
    with tab2:
        st.subheader("🔬 Advanced Graph Analytics")

        # ----------------------------
        # 1. SHORTEST PATH
        # ----------------------------
        st.markdown("### 🛤️ Shortest Path Analysis")

        # Load book titles for dropdown
        if 'book_titles' not in st.session_state:
            try:
                book_records = run_neo4j_read(get_all_book_titles, limit=1000)
                st.session_state.book_titles = [b["title"] for b in book_records]
            except:
                st.session_state.book_titles = []
        
        book_titles = st.session_state.book_titles

        col1, col2 = st.columns(2)
        with col1:
            default_book1 = "The Hunger Games (The Hunger Games, #1)"
            default_idx1 = book_titles.index(default_book1) if default_book1 in book_titles else 0
            book1 = st.selectbox(
                "📘 Starting Book",
                book_titles,
                index=default_idx1,
                key="sp_book1",
            )
        with col2:
            default_book2 = "Divergent (Divergent, #1)"
            default_idx2 = book_titles.index(default_book2) if default_book2 in book_titles else 1
            book2 = st.selectbox(
                "📗 Destination Book",
                book_titles,
                index=default_idx2,
                key="sp_book2",
            )

        if st.button("🔍 Find Connection Path", use_container_width=True):
            try:
                with driver.session() as session:
                    path_records = session.execute_read(
                        get_shortest_path, book1, book2
                    )

                if path_records:
                    record = dict(path_records[0])
                    nodes = record.get("path_nodes", [])
                    hops = record.get("hops", None)

                    if nodes:
                        st.success("✓ Connection path discovered!")
                        st.write("### 🗺️ Connection Path:")
                        st.write(" → ".join(nodes))
                        if hops is not None:
                            st.metric("Degrees of Separation", hops)
                    else:
                        st.warning("Path exists but details unavailable.")
                else:
                    st.info("No connection path found between these books.")
            except Exception as e:
                st.error(f"Analysis error: {e}")

        st.markdown("---")

        # ----------------------------
        # 2. CENTRALITY
        # ----------------------------
        st.markdown("### 👥 Author Influence Analysis")

        # Genre/Tag filter for authors
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            # Get all tags for filter
            all_tags_records = run_neo4j_read(get_all_tags)
            tag_options = ["All Genres"] + [t["tag"] for t in all_tags_records]
            
            selected_genre = st.selectbox(
                "Filter by Genre/Tag",
                tag_options,
                key="genre_filter"
            )
        
        with col_b:
            sort_by = st.selectbox(
                "Sort Criteria",
                ["Most Prolific", "Highest Rated"],
                key="author_sort"
            )

        if st.button("📊 Analyze Authors", key="show_centrality_btn", use_container_width=True):
            try:
                with driver.session() as session:
                    if selected_genre == "All Genres":
                        # Show top authors overall
                        top_authors_records = session.execute_read(get_top_authors, limit=100)
                        authors_df = pd.DataFrame([dict(r) for r in top_authors_records])
                    else:
                        # Show authors filtered by genre
                        authors_by_genre = session.execute_read(get_authors_by_tag, selected_genre, limit=100)
                        authors_df = pd.DataFrame([dict(r) for r in authors_by_genre])
                    
                    if not authors_df.empty:
                        # Apply sorting
                        if sort_by == "Highest Rated" and 'avg_rating' in authors_df.columns:
                            authors_df = authors_df.sort_values('avg_rating', ascending=False)
                        
                        genre_text = f" in {selected_genre}" if selected_genre != "All Genres" else ""
                        st.write(f"### 📊 Top Authors{genre_text}")
                        st.dataframe(authors_df, use_container_width=True, height=400)
                        
                        # Show count
                        st.caption(f"Displaying {len(authors_df)} authors | Sorted by: {sort_by}")
                    else:
                        st.warning("No authors found for the selected genre.")
                        
            except Exception as e:
                st.error(f"Error running query: {e}")
        
        st.markdown("---")
        
        # Show top tags separately
        if st.button("🏷️ View Top Tags & Genres", key="show_tags_btn", use_container_width=True):
            try:
                with driver.session() as session:
                    top_tags_records = session.execute_read(get_top_tags, limit=50)
                    tags_df = pd.DataFrame([dict(r) for r in top_tags_records])
                
                st.write("### 🏷️ Most Popular Tags/Genres")
                st.dataframe(tags_df, use_container_width=True, height=400)
                st.caption(f"Displaying top {len(tags_df)} tags by book count")
            except Exception as e:
                st.error(f"Analysis error: {e}")

        st.markdown("---")

        # ----------------------------
        # 3. TRAVERSAL
        # ----------------------------
        st.markdown("### 🔀 Book Relationship Explorer")

        default_trav = "The Hunger Games (The Hunger Games, #1)"
        default_idx_trav = book_titles.index(default_trav) if default_trav in book_titles else 0
        traversal_title = st.selectbox(
            "Select Book to Explore",
            book_titles,
            index=default_idx_trav,
            key="traversal_title",
        )

        col3, col4 = st.columns(2)
        with col3:
            if st.button("🏷️ Find by Similar Tags", use_container_width=True):
                try:
                    with driver.session() as session:
                        related_tag_records = session.execute_read(
                            get_related_books_by_tags, traversal_title
                        )
                    related_tag_df = pd.DataFrame(
                        [dict(r) for r in related_tag_records]
                    )
                    st.write("### 📚 Books with Similar Tags")
                    st.dataframe(related_tag_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Query error: {e}")

        with col4:
            if st.button("✍️ Find by Same Author", use_container_width=True):
                try:
                    with driver.session() as session:
                        related_author_records = session.execute_read(
                            get_related_books_by_author, traversal_title
                        )
                    related_author_df = pd.DataFrame(
                        [dict(r) for r in related_author_records]
                    )
                    st.write("### 📖 Other Works by This Author")
                    st.dataframe(related_author_df, use_container_width=True)
                except Exception as e:
                    st.error(f"Query error: {e}")


# ------------------------------
# SQL PAGE
# ------------------------------
def sql_page():
    st.header("📊 Relational Database Analytics")

    # Create tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Database Overview", "👥 Author Analytics", "📈 Publication Trends", "⭐ Rating Analysis"])

    # ============================================================
    # TAB 1 – OVERVIEW
    # ============================================================
    with tab1:
        st.subheader("📈 Database Statistics")
        
        # Get basic stats
        try:
            from sqlalchemy import text
            engine = sql.get_engine()
            
            with engine.connect() as conn:
                book_count = conn.execute(text("SELECT COUNT(*) FROM books")).scalar()
                user_count = conn.execute(text("SELECT COUNT(DISTINCT user_id) FROM ratings")).scalar()
                rating_count = conn.execute(text("SELECT COUNT(*) FROM ratings")).scalar()
            
            st.markdown("### 📊 Collection Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Books in Catalog", f"{book_count:,}")
            col2.metric("Active Users", f"{user_count:,}")
            col3.metric("Total Ratings", f"{rating_count:,}")
            
        except Exception as e:
            st.error(f"Database error: {e}")
        
        st.markdown("---")
        
        # Top Rated Books with better controls
        st.subheader("⭐ Top-Rated Books Analysis")
        
        col_a, col_b = st.columns([3, 1])
        with col_a:
            min_ratings = st.slider("Minimum Rating Count", 50, 5000, 500, 50, key="top_rated_slider")
        with col_b:
            num_books = st.selectbox("Show Top", [25, 50, 100, 200], index=1, key="num_top_books")
        
        top_books = sql.get_top_rated_books(limit=num_books, min_ratings=min_ratings)
        if not top_books.empty:
            # Add ranking column
            top_books_display = top_books.copy()
            top_books_display.insert(0, 'Rank', range(1, len(top_books_display) + 1))
            
            st.dataframe(top_books_display, use_container_width=True, height=400)
            st.caption(f"📊 Showing {len(top_books)} books with ≥{min_ratings:,} ratings | Sorted by average rating")
        else:
            st.info(f"No books found with at least {min_ratings:,} ratings. Try lowering the threshold.")
        
        st.markdown("---")
        
        # Most Rated Books
        st.subheader("🔥 Most Reviewed Books")
        num_popular = st.selectbox("Number of Books to Display", [20, 50, 100], index=1, key="num_popular")
        most_rated = sql.get_most_rated_books(limit=num_popular)
        if not most_rated.empty:
            most_rated_display = most_rated.copy()
            most_rated_display.insert(0, 'Rank', range(1, len(most_rated_display) + 1))
            st.dataframe(most_rated_display, use_container_width=True, height=400)
            st.caption(f"📊 Top {len(most_rated)} books by review volume | Useful for identifying trending titles")

    # ============================================================
    # TAB 2 – AUTHORS
    # ============================================================
    with tab2:
        st.subheader("👥 Author Performance Metrics")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            limit = st.slider("Number of Authors to Display", 10, 100, 50, 10, key="author_limit")
        with col2:
            show_chart = st.checkbox("Show Visualization", value=True, key="show_author_chart")
        
        top_authors_df = sql.get_top_authors(limit=limit)
        
        if not top_authors_df.empty:
            # Add ranking
            top_authors_display = top_authors_df.copy()
            top_authors_display.insert(0, 'Rank', range(1, len(top_authors_display) + 1))
            st.dataframe(top_authors_display, use_container_width=True, height=400)
            st.caption(f"📊 Top {len(top_authors_df)} authors by catalog presence")
            
            # Visualization
            if show_chart:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 6))
                display_count = min(15, len(top_authors_df))
                ax.barh(top_authors_df['authors'][:display_count], top_authors_df['book_count'][:display_count])
                ax.set_xlabel('Number of Published Books')
                ax.set_ylabel('Author Name')
                ax.set_title(f'Top {display_count} Most Prolific Authors')
                ax.invert_yaxis()
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("No author data available in the database.")

    # ============================================================
    # TAB 3 – TRENDS
    # ============================================================
    with tab3:
        st.subheader("📅 Historical Publication Analysis")
        
        trends = sql.get_publication_trends()
        
        if not trends.empty:
            st.markdown("### 📈 Publications Over Time")
            st.line_chart(trends.set_index('year')['book_count'])
            st.caption("Number of books published per year (1900-2025)")
            
            st.markdown("---")
            st.subheader("🌍 Language Distribution")
            
            lang_data = sql.get_books_by_language()
            if not lang_data.empty:
                st.dataframe(lang_data.head(20), use_container_width=True)
                
                # Bar chart
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 6))
                top_langs = lang_data.head(10)
                ax.bar(top_langs['language_code'], top_langs['book_count'])
                ax.set_xlabel('Language Code (ISO 639)')
                ax.set_ylabel('Book Count')
                ax.set_title('Top 10 Languages in Catalog')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                st.caption("Distribution of books by language code")
        else:
            st.info("Publication trend data not available.")

    # ============================================================
    # TAB 4 – RATINGS
    # ============================================================
    with tab4:
        st.subheader("⭐ User Rating Insights")
        
        # Rating distribution
        rating_dist = sql.get_rating_distribution()
        
        if not rating_dist.empty:
            st.markdown("### 📊 Rating Distribution Across Catalog")
            st.bar_chart(rating_dist.set_index('rating_bucket')['book_count'])
            st.caption("Distribution of average book ratings (0.0 - 5.0 scale)")
            
            st.markdown("---")
            
            # User rating stats
            st.subheader("🏆 Top Contributors")
            user_stats = sql.get_user_rating_stats(limit=20)
            if not user_stats.empty:
                st.dataframe(user_stats, use_container_width=True)
                st.caption("Most active users by number of ratings submitted")
        else:
            st.info("Rating analytics data not available.")
        
        st.markdown("---")
        
        # Book search - more business relevant
        st.subheader("🔍 Advanced Book Search & Filtering")
        
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            search_keyword = st.text_input("Search by Title or Author Name", "", key="sql_search", placeholder="Enter keywords (leave empty for all)...")
        with col_s2:
            search_limit = st.selectbox("Max Results", [50, 100, 200, 500], index=1, key="search_limit")
        
        min_rating_filter = st.slider("Minimum Rating Threshold", 0.0, 5.0, 3.0, 0.1, key="sql_min_rating")
        
        if st.button("🔍 Execute Search", key="sql_search_btn", use_container_width=True):
            search_results = sql.search_books(keyword=search_keyword if search_keyword else "", min_rating=min_rating_filter)
            
            # Limit results to selected amount
            if not search_results.empty:
                search_results = search_results.head(search_limit)
                search_display = search_results.copy()
                search_display.insert(0, 'Rank', range(1, len(search_display) + 1))
                
                st.dataframe(search_display, use_container_width=True, height=500)
                st.caption(f"📊 Found {len(search_results)} books | Rating ≥ {min_rating_filter} | Business Insight: Use for inventory decisions")
            else:
                st.info("No books match the specified search criteria. Try adjusting the rating threshold.")


# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    main()
