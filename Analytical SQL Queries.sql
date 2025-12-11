/*******************************************************
* MGTA603 FINAL PROJECT — SQL ANALYTICS COMPONENT
* Description:
*   - Create normalized schema
*   - Define keys and relationships
*   - Import 5 CSV datasets
*   - Implement analytical queries (JOIN, AGG, Subquery)
*   - Create one stored procedure and one view
*******************************************************/

-- Use project database
USE goodbooks;


---------------------------------------------------------
-- PART 1: CREATE TABLES (Your specified schema)
---------------------------------------------------------

-- Books table
CREATE TABLE books (
    book_id INT PRIMARY KEY,
    goodreads_book_id INT UNIQUE,
    best_book_id INT,
    work_id INT,
    books_count INT,
    isbn VARCHAR(20),
    isbn13 BIGINT,
    authors VARCHAR(1000),
    original_publication_year INT,
    original_title VARCHAR(1000),
    title VARCHAR(1000),
    language_code VARCHAR(20),
    average_rating DECIMAL(3,2),
    ratings_count INT,
    work_ratings_count INT,
    work_text_reviews_count INT,
    ratings_1 INT,
    ratings_2 INT,
    ratings_3 INT,
    ratings_4 INT,
    ratings_5 INT,
    image_url VARCHAR(500),
    small_image_url VARCHAR(500)
);

-- Tags table
CREATE TABLE tags (
    tag_id INT PRIMARY KEY,
    tag_name VARCHAR(200)
);

-- Book–Tag mapping (many-to-many)
CREATE TABLE book_tags (
    goodreads_book_id INT,
    tag_id INT,
    count INT,
    FOREIGN KEY (goodreads_book_id) REFERENCES books(goodreads_book_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- User ratings
CREATE TABLE ratings (
    user_id INT,
    book_id INT,
    rating INT,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

-- User reading list
CREATE TABLE to_read (
    user_id INT,
    book_id INT,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);



---------------------------------------------------------
-- PART 2: IMPORT DATA
-- 
-- IMPORTANT: Update the file paths below to match your local setup.
-- CSV files should be located in the Dashboard603/data/ directory.
--
-- To import data:
-- 1. Start MySQL with local infile enabled:
--        mysql -u root -p --local-infile=1
--
-- 2. Verify LOCAL INFILE is enabled:
--        SHOW VARIABLES LIKE 'local_infile';
--
-- 3. Update the paths below to point to your CSV files, then run:
--        LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/books.csv'
--        INTO TABLE books
--        FIELDS TERMINATED BY ','
--        ENCLOSED BY '"'
--        IGNORE 1 ROWS;
--
-- Note: On macOS, MySQL Workbench may block LOCAL INFILE for security.
-- Use the MySQL terminal client instead.
---------------------------------------------------------

-- Example import commands (update paths as needed):
-- LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/books.csv'
-- INTO TABLE books
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 ROWS;
--
-- LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/tags.csv'
-- INTO TABLE tags
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 ROWS;
--
-- LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/book_tags.csv'
-- INTO TABLE book_tags
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 ROWS;
--
-- LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/ratings.csv'
-- INTO TABLE ratings
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 ROWS;
--
-- LOAD DATA LOCAL INFILE '/path/to/Dashboard603/data/to_read.csv'
-- INTO TABLE to_read
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 ROWS;



---------------------------------------------------------
-- PART 3: ANALYTICAL QUERIES
---------------------------------------------------------

-------------------------
-- JOIN QUERY 1
-- Book titles with their tags
-------------------------
SELECT b.title, t.tag_name, bt.count
FROM books b
JOIN book_tags bt ON b.goodreads_book_id = bt.goodreads_book_id
JOIN tags t ON t.tag_id = bt.tag_id
ORDER BY bt.count DESC
LIMIT 20;

-- ---------------------------------------------------------
-- JOIN QUERY 2
-- User with rated books
-- ---------------------------------------------------------
SELECT r.user_id, b.title, r.rating
FROM ratings r
JOIN books b ON r.book_id = b.book_id
ORDER BY r.rating DESC
LIMIT 20;

-- ---------------------------------------------------------
-- JOIN QUERY 3
-- Most frequent tags
-- ---------------------------------------------------------
SELECT t.tag_name, SUM(bt.count) AS total_usage
FROM tags t
JOIN book_tags bt ON t.tag_id = bt.tag_id
GROUP BY t.tag_id
ORDER BY total_usage DESC
LIMIT 10;



-- ---------------------------------------------------------
-- PART 4: AGGREGATION QUERIES
-- ---------------------------------------------------------

-- AGG #1: Most-rated books
SELECT title, ratings_count
FROM books
ORDER BY ratings_count DESC
LIMIT 10;

-- AGG #2: Books with high average rating grouped by year
SELECT original_publication_year, COUNT(*) AS book_count
FROM books
WHERE average_rating > 4.3
GROUP BY original_publication_year
HAVING book_count > 5
ORDER BY book_count DESC;



-- ---------------------------------------------------------
-- PART 5: SUBQUERY
-- ---------------------------------------------------------

-- Books with above-average rating
SELECT *
FROM books
WHERE average_rating >
      (SELECT AVG(average_rating) FROM books)
ORDER BY average_rating DESC;



-- ---------------------------------------------------------
-- PART 6: STORED PROCEDURE
-- ---------------------------------------------------------

DELIMITER $$

-- Procedure: Get top books rated by a specific user
CREATE PROCEDURE GetTopBooksByUser(IN uid INT)
BEGIN
    SELECT b.title, r.rating
    FROM ratings r
    JOIN books b ON r.book_id = b.book_id
    WHERE r.user_id = uid
    ORDER BY r.rating DESC
    LIMIT 10;
END $$

DELIMITER ;



-- ---------------------------------------------------------
-- PART 7: VIEW
-- ---------------------------------------------------------


-- View combining books and their tags
CREATE VIEW book_with_tags AS
SELECT b.book_id, b.title, t.tag_name
FROM books b
JOIN book_tags bt ON b.goodreads_book_id = bt.goodreads_book_id
JOIN tags t ON t.tag_id = bt.tag_id;

-- Example usage:
-- SELECT * FROM book_with_tags LIMIT 20;

