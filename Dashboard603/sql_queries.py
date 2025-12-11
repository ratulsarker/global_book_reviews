"""
SQL queries for Goodbooks database analytics.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import config


def get_engine():
    """Get SQL database engine."""
    return create_engine(config.SQL_CONNECTION_STRING)


def get_top_authors(limit=10):
    """
    Get top authors by number of books.
    
    Dashboard Location: SQL Database Analytics > Author Analytics tab
    Displays the most prolific authors sorted by number of books published.
    """
    engine = get_engine()
    query = """
    SELECT 
        authors,
        COUNT(*) as book_count,
        ROUND(AVG(average_rating), 2) as avg_rating,
        SUM(ratings_count) as total_ratings
    FROM books
    WHERE authors IS NOT NULL AND authors != ''
    GROUP BY authors
    ORDER BY book_count DESC, avg_rating DESC
    LIMIT :limit
    """
    try:
        df = pd.read_sql(text(query), engine, params={"limit": limit})
        return df
    except Exception as e:
        print(f"Error in get_top_authors: {e}")
        return pd.DataFrame()


def get_rating_distribution():
    """
    Get distribution of average ratings.
    
    Dashboard Location: SQL Database Analytics > Rating Analysis tab > Rating Distribution Across Catalog
    Shows a bar chart of how books are distributed across different rating buckets (0.0-5.0 scale).
    """
    engine = get_engine()
    query = """
    SELECT 
        ROUND(average_rating, 1) as rating_bucket,
        COUNT(*) as book_count
    FROM books
    GROUP BY rating_bucket
    ORDER BY rating_bucket
    """
    try:
        df = pd.read_sql(text(query), engine)
        return df
    except Exception as e:
        print(f"Error in get_rating_distribution: {e}")
        return pd.DataFrame()


def get_top_rated_books(limit=20, min_ratings=1000):
    """
    Get top-rated books with minimum ratings.
    
    Dashboard Location: SQL Database Analytics > Database Overview tab > Top-Rated Books Analysis
    Displays books with the highest average ratings, filtered by minimum number of ratings.
    """
    engine = get_engine()
    query = """
    SELECT 
        title,
        authors,
        average_rating,
        ratings_count,
        original_publication_year
    FROM books
    WHERE ratings_count >= :min_ratings
    ORDER BY average_rating DESC, ratings_count DESC
    LIMIT :limit
    """
    try:
        df = pd.read_sql(text(query), engine, params={"limit": limit, "min_ratings": min_ratings})
        return df
    except Exception as e:
        print(f"Error in get_top_rated_books: {e}")
        return pd.DataFrame()


def get_most_rated_books(limit=20):
    """
    Get books with the most ratings.
    
    Dashboard Location: SQL Database Analytics > Database Overview tab > Most Reviewed Books
    Shows books sorted by total number of ratings (review volume), useful for identifying trending titles.
    """
    engine = get_engine()
    query = """
    SELECT 
        title,
        authors,
        ratings_count,
        average_rating,
        original_publication_year
    FROM books
    ORDER BY ratings_count DESC
    LIMIT :limit
    """
    try:
        df = pd.read_sql(text(query), engine, params={"limit": limit})
        return df
    except Exception as e:
        print(f"Error in get_most_rated_books: {e}")
        return pd.DataFrame()


def get_books_by_language():
    """
    Get book distribution by language.
    
    Dashboard Location: SQL Database Analytics > Publication Trends tab > Language Distribution
    Displays the distribution of books by language code with a bar chart showing top 10 languages.
    """
    engine = get_engine()
    query = """
    SELECT 
        language_code,
        COUNT(*) as book_count,
        ROUND(AVG(average_rating), 2) as avg_rating
    FROM books
    WHERE language_code IS NOT NULL AND language_code != ''
    GROUP BY language_code
    ORDER BY book_count DESC
    """
    try:
        df = pd.read_sql(text(query), engine)
        return df
    except Exception as e:
        print(f"Error in get_books_by_language: {e}")
        return pd.DataFrame()


def get_publication_trends():
    """
    Get publication trends over years.
    
    Dashboard Location: SQL Database Analytics > Publication Trends tab > Publications Over Time
    Shows a line chart of the number of books published per year from 1900-2025.
    """
    engine = get_engine()
    query = """
    SELECT 
        CAST(original_publication_year AS SIGNED) as year,
        COUNT(*) as book_count,
        ROUND(AVG(average_rating), 2) as avg_rating
    FROM books
    WHERE original_publication_year IS NOT NULL 
        AND original_publication_year > 1900 
        AND original_publication_year <= 2025
    GROUP BY year
    ORDER BY year
    """
    try:
        df = pd.read_sql(text(query), engine)
        return df
    except Exception as e:
        print(f"Error in get_publication_trends: {e}")
        return pd.DataFrame()


def get_user_rating_stats(limit=20):
    """
    Get statistics about most active users.
    
    Dashboard Location: SQL Database Analytics > Rating Analysis tab > Top Contributors
    Displays the most active users by number of ratings submitted, including their average rating patterns.
    """
    engine = get_engine()
    query = """
    SELECT 
        user_id,
        COUNT(*) as books_rated,
        ROUND(AVG(rating), 2) as avg_rating_given,
        MIN(rating) as min_rating,
        MAX(rating) as max_rating
    FROM ratings
    GROUP BY user_id
    ORDER BY books_rated DESC
    LIMIT :limit
    """
    try:
        df = pd.read_sql(text(query), engine, params={"limit": limit})
        return df
    except Exception as e:
        print(f"Error in get_user_rating_stats: {e}")
        return pd.DataFrame()


def search_books(keyword="", min_rating=0.0):
    """
    Search books by title or author.
    
    Dashboard Location: SQL Database Analytics > Rating Analysis tab > Advanced Book Search & Filtering
    Allows users to search for books by title or author name with optional minimum rating filter.
    """
    engine = get_engine()
    query = """
    SELECT 
        title,
        authors,
        average_rating,
        ratings_count,
        original_publication_year
    FROM books
    WHERE (LOWER(title) LIKE LOWER(:keyword) OR LOWER(authors) LIKE LOWER(:keyword))
        AND average_rating >= :min_rating
    ORDER BY ratings_count DESC
    LIMIT 50
    """
    try:
        df = pd.read_sql(text(query), engine, params={"keyword": f"%{keyword}%", "min_rating": min_rating})
        return df
    except Exception as e:
        print(f"Error in search_books: {e}")
        return pd.DataFrame()
