# 📚 Goodbooks Analytics Platform

A hybrid database analytics dashboard using Neo4j (graph database) and MySQL (relational database) to analyze book ratings, recommendations, and user behavior.

## 📊 Research Poster

**GLOBAL BOOK REVIEWS: Multi-Database Analytics for Personalized Book Discovery**

*Authors: Jiaxi Wang, Mohammad Al-Maghaireh, Ratul Sarker*  
*Lazaridis School of Business & Economics, Wilfrid Laurier University*

![Research Poster](assets/poster.png)

## Overview

This project demonstrates the integration of two database paradigms:
- **Neo4j**: Graph analysis, book recommendations, shortest path algorithms
- **MySQL**: Relational analytics, trends, author statistics, aggregations

## Prerequisites

- **Neo4j** database running (with dump file loaded)
- **MySQL** database running (with SQL schema and data imported)
- Python 3.7+

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd Dashboard603
pip3 install -r requirements.txt --user
```

Or using a virtual environment (recommended):
```bash
cd Dashboard603
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Database Connections

Edit `Dashboard603/config.py` and update:
- **Neo4j password**: Change `NEO4J_PASSWORD` to match your Neo4j instance
- **MySQL password**: Change `MYSQL_PASSWORD` to match your MySQL instance
- **Neo4j database name**: Check `neo4j_queries.py` line 14 - ensure the database name matches your loaded dump
- **MySQL database name**: Should be `goodbooks` (or your actual database name)

### 3. Set Up Databases

#### Neo4j Setup
1. Start Neo4j Desktop
2. Create a new database or use an existing one
3. Load the dump file: `goodbooks-2025-11-20T18-16-45.dump`
4. Verify the database name matches the one in `neo4j_queries.py`

#### MySQL Setup
1. Start MySQL server
2. Create the database: `CREATE DATABASE goodbooks;`
3. Run the SQL file: `Analytical SQL Queries.sql` to create tables
4. Import CSV data from `Dashboard603/data/` directory:
   - Update file paths in the SQL file to match your local setup
   - Use `LOAD DATA LOCAL INFILE` commands (see SQL file for instructions)

### 4. Run the Application

```bash
cd Dashboard603
python3 -m streamlit run app.py
```

Or use the provided script:
```bash
./RUN.sh
```

### 5. Access the Dashboard

Open your browser and navigate to: **http://localhost:8501**

## Features

### Neo4j Graph Database
- Graph visualization of book relationships
- Book recommendations based on user preferences
- Shortest path analysis between books
- Tag-based book discovery

### MySQL Relational Database
- Analytical queries with JOINs, aggregations, and subqueries
- Author statistics and trends
- Publication year analysis
- User rating patterns
- Stored procedures and views

## Project Structure

```
project_603/
├── Dashboard603/
│   ├── app.py                 # Main Streamlit application
│   ├── config.py              # Database configuration
│   ├── neo4j_queries.py       # Neo4j query functions
│   ├── sql_queries.py         # MySQL query functions
│   ├── graph_utils.py         # Graph visualization utilities
│   ├── requirements.txt       # Python dependencies
│   ├── data/                  # CSV data files
│   │   ├── books.csv
│   │   ├── tags.csv
│   │   ├── book_tags.csv
│   │   └── to_read.csv
│   └── lib/                   # JavaScript libraries
├── Analytical SQL Queries.sql # MySQL schema and queries
├── goodbooks-*.dump           # Neo4j database dump
├── assets/                    # Images and media files
│   └── poster.png             # Research poster
├── RUN.sh                     # Quick start script
└── README.md                  # This file
```

## Data

The dataset includes:
- **10,000 books** with metadata
- **6 million ratings** from users
- **34,000+ tags** for categorization
- User reading lists and preferences

## Troubleshooting

### Connection Errors

**Neo4j:**
- Ensure Neo4j is running on `bolt://localhost:7687`
- Verify the database name in `neo4j_queries.py` matches your Neo4j database
- Check that the dump file has been loaded successfully

**MySQL:**
- Ensure MySQL is running on `localhost`
- Verify the database `goodbooks` exists
- Check that all tables have been created and data imported

### Import Errors

If you see module import errors:
```bash
pip3 install streamlit neo4j pandas pyvis sqlalchemy matplotlib pymysql --user
```

### Database Not Found

- **Neo4j**: Check that the dump file has been loaded into your Neo4j instance
- **MySQL**: Verify the SQL file has been imported and the database exists

## License

See LICENSE file for details.
