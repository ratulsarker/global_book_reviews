# 🏗️ Goodbooks Analytics Platform - System Architecture

## Executive Summary

The Goodbooks Analytics Platform is a **hybrid database architecture** that leverages both **relational (MySQL)** and **graph (Neo4j)** databases to provide comprehensive book analytics and recommendation capabilities. The system uses a Streamlit web dashboard as the frontend interface that queries both databases simultaneously.

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB DASHBOARD                        │
│                    (Python Application)                           │
│                    http://localhost:8501                          │
└──────────────┬──────────────────────────────┬────────────────────┘
               │                              │
               │                              │
    ┌──────────▼──────────┐      ┌───────────▼──────────┐
    │   MySQL Database    │      │   Neo4j Database     │
    │   (Relational)      │      │   (Graph)            │
    │   Port: 3306        │      │   Port: 7687         │
    │                     │      │                      │
    │   Database:         │      │   Database:          │
    │   goodbooks         │      │   goodbooks-2025-... │
    └─────────────────────┘      └──────────────────────┘
```

---

## Component Breakdown

### 1. **MySQL Database (Relational Database)**

**Purpose**: Structured analytics, aggregations, and trend analysis

**Technology Stack**:
- Database Engine: MySQL Server
- Connection: PyMySQL + SQLAlchemy
- Port: 3306 (default)
- Database Name: `goodbooks`

**Schema Structure**:
- **books**: Core book information (10,000 books)
  - Primary Key: `book_id`
  - Fields: title, authors, ratings, publication year, language, etc.
- **tags**: Book tags/genres (34,000+ tags)
  - Primary Key: `tag_id`
- **book_tags**: Many-to-many relationship between books and tags
- **ratings**: User ratings (6 million ratings)
- **to_read**: User reading lists

**Key Capabilities**:
- ✅ Complex JOIN operations
- ✅ Aggregations (COUNT, AVG, SUM)
- ✅ Subqueries and window functions
- ✅ Stored procedures and views
- ✅ Publication trend analysis
- ✅ Author performance metrics
- ✅ Rating distribution analytics

**Connection Details**:
```python
Connection String: mysql+pymysql://root:password@localhost/goodbooks
```

---

### 2. **Neo4j Database (Graph Database)**

**Purpose**: Graph-based queries, recommendations, and relationship traversal

**Technology Stack**:
- Database Engine: Neo4j Community Edition
- Connection: Neo4j Python Driver (Bolt Protocol)
- Port: 7687 (Bolt protocol)
- Database Name: `goodbooks-2025-11-20t18-16-45`

**Graph Schema**:
```
Nodes:
  - Book {title, average_rating, ratings_count}
  - Tag {name}
  - Author {name}

Relationships:
  - (Book)-[:TAGGED_AS]->(Tag)
  - (Book)-[:WRITTEN_BY]->(Author)
```

**Key Capabilities**:
- ✅ Graph pattern matching
- ✅ Shortest path algorithms
- ✅ Community detection (book recommendations)
- ✅ Tag-based similarity analysis
- ✅ Author influence analysis
- ✅ Network visualization

**Connection Details**:
```python
URI: bolt://localhost:7687
Protocol: Bolt
Database: goodbooks-2025-11-20t18-16-45
```

---

### 3. **Streamlit Dashboard Application**

**Purpose**: Web-based user interface for querying and visualizing data

**Technology Stack**:
- Framework: Streamlit
- Language: Python 3.12
- Port: 8501 (default)
- Location: `Dashboard603/app.py`

**Application Structure**:
```
Dashboard603/
├── app.py              # Main Streamlit application
├── config.py           # Database connection configuration
├── neo4j_queries.py    # Neo4j query functions
├── sql_queries.py      # MySQL query functions
├── graph_utils.py      # Graph visualization utilities
└── requirements.txt    # Python dependencies
```

**Key Features**:
- **Graph Database Insights Tab**:
  - Book discovery by genre/tag
  - Personalized recommendations
  - Network graph visualization
  - Shortest path analysis
  - Author influence metrics
  
- **SQL Database Analytics Tab**:
  - Database overview statistics
  - Author performance analytics
  - Publication trends over time
  - Rating distribution analysis
  - Advanced book search

**Dependencies**:
```
streamlit      # Web framework
neo4j          # Neo4j driver
pandas         # Data manipulation
pyvis          # Graph visualization
sqlalchemy     # SQL toolkit
matplotlib     # Plotting
pymysql        # MySQL connector
```

---

## Data Flow

### 1. **Initial Data Loading**

```
CSV Files → MySQL Import → MySQL Database
    ↓
CSV Files → Neo4j Import → Neo4j Database
```

**Data Sources**:
- `books.csv` (10,000 books)
- `tags.csv` (34,000+ tags)
- `book_tags.csv` (book-tag relationships)
- `ratings.csv` (6 million ratings)
- `to_read.csv` (user reading lists)

### 2. **Runtime Query Flow**

```
User Interaction (Browser)
    ↓
Streamlit Dashboard (app.py)
    ↓
    ├─→ neo4j_queries.py → Neo4j Database (Graph Queries)
    │
    └─→ sql_queries.py → MySQL Database (Analytical Queries)
    ↓
Results Aggregated & Displayed
```

---

## Prerequisites & Startup Sequence

### ⚠️ **CRITICAL: Databases Must Be Running Before Dashboard**

The system requires **both databases to be running in the background** before starting the Streamlit application.

### Step 1: Start MySQL Database

**Option A - MySQL Service (macOS)**:
```bash
# Check if MySQL is running
brew services list | grep mysql

# Start MySQL if not running
brew services start mysql

# Or use system service
sudo /usr/local/mysql/support-files/mysql.server start
```

**Option B - Verify MySQL is Running**:
```bash
# Check if port 3306 is listening
lsof -i :3306

# Test connection
mysql -u root -p -e "SHOW DATABASES;"
```

**Database Setup** (if not already done):
```bash
# Import schema and data
mysql -u root -p < Analytical\ SQL\ Queries.sql
```

---

### Step 2: Start Neo4j Database

**Using Neo4j Desktop**:
1. Open Neo4j Desktop application
2. Select instance: **"603_project"**
3. Click **Play button (▶️)** to start the instance
4. Wait for status to change to **"RUNNING"**
5. Verify database: `goodbooks-2025-11-20t18-16-45` exists

**Verify Neo4j is Running**:
```bash
# Check if port 7687 is listening
lsof -i :7687

# Test connection (using Python)
python3 -c "from neo4j import GraphDatabase; \
driver = GraphDatabase.driver('bolt://localhost:7687', \
auth=('neo4j', 'your_password')); \
driver.verify_connectivity(); print('✅ Connected')"
```

**Important Notes**:
- Neo4j instance must be **RUNNING** (not STOPPED)
- Database name must match: `goodbooks-2025-11-20t18-16-45`
- Port 7687 must be available (no other Neo4j instance using it)

---

### Step 3: Configure Database Credentials

Edit `Dashboard603/config.py`:
```python
# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_neo4j_password"  # ⚠️ Update this

# MySQL Configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_mysql_password"  # ⚠️ Update this
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "goodbooks"
```

Also update `Dashboard603/neo4j_queries.py` (line 9):
```python
NEO4J_PASSWORD = "your_neo4j_password"  # ⚠️ Update this
```

---

### Step 4: Install Python Dependencies

```bash
cd Dashboard603
pip3 install -r requirements.txt --user
```

---

### Step 5: Start Streamlit Dashboard

```bash
cd Dashboard603
python3 -m streamlit run app.py
```

**Or use the provided script**:
```bash
./RUN.sh
```

**Access Dashboard**: http://localhost:8501

---

## System Requirements

### Hardware Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: ~2GB for databases and data
- **CPU**: Multi-core recommended for concurrent queries

### Software Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **MySQL**: 5.7+ or 8.0+
- **Neo4j**: 4.0+ (Community Edition)
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Network Requirements
- **Ports**:
  - `3306`: MySQL (must be available)
  - `7687`: Neo4j Bolt protocol (must be available)
  - `8501`: Streamlit web server (must be available)

---

## Architecture Benefits

### Why Hybrid Architecture?

1. **MySQL (Relational)**:
   - ✅ Excellent for structured analytics
   - ✅ Fast aggregations and JOINs
   - ✅ ACID compliance for data integrity
   - ✅ Mature ecosystem and tools

2. **Neo4j (Graph)**:
   - ✅ Natural representation of relationships
   - ✅ Efficient graph traversal queries
   - ✅ Built-in graph algorithms
   - ✅ Intuitive for recommendation systems

3. **Combined Power**:
   - ✅ Best of both worlds
   - ✅ Use each database for its strengths
   - ✅ Comprehensive analytics capabilities

---

## Query Distribution

### MySQL Handles:
- Database statistics and counts
- Author performance metrics
- Publication trends over time
- Rating distributions
- Complex aggregations
- Language analysis
- User rating statistics

### Neo4j Handles:
- Book recommendations based on shared tags
- Shortest path between books
- Tag-based book discovery
- Author influence analysis
- Graph network visualization
- Community detection
- Relationship traversal

---

## Security Considerations

1. **Database Credentials**: Stored in `config.py` (consider using environment variables in production)
2. **Network**: All connections are localhost (no external network exposure)
3. **Authentication**: Both databases require username/password authentication
4. **Port Access**: Only localhost connections allowed by default

---

## Troubleshooting

### Common Issues:

1. **"Neo4j connection failed"**:
   - Verify Neo4j instance is RUNNING (not STOPPED)
   - Check port 7687 is not blocked
   - Verify database name matches
   - Check password in config files

2. **"MySQL connection failed"**:
   - Verify MySQL service is running
   - Check port 3306 is available
   - Verify database `goodbooks` exists
   - Check password in config.py

3. **"Port already in use"**:
   - Another instance may be running
   - Stop conflicting services
   - Check with `lsof -i :PORT_NUMBER`

---

## Performance Characteristics

- **MySQL Queries**: Typically < 100ms for aggregations
- **Neo4j Queries**: Typically < 500ms for graph traversals
- **Dashboard Load Time**: < 2 seconds initial load
- **Graph Visualization**: 1-3 seconds for network generation

---

## Future Enhancements

- [ ] Add Redis caching layer
- [ ] Implement connection pooling optimization
- [ ] Add real-time data synchronization
- [ ] Deploy to cloud infrastructure
- [ ] Add user authentication
- [ ] Implement API endpoints

---

## References

- **Project Repository**: `/Users/ocean/Downloads/project_603/`
- **MySQL Schema**: `Analytical SQL Queries.sql`
- **Neo4j Dump**: `goodbooks-2025-11-20T18-16-45.dump`
- **Documentation**: `README.md`, `QUICK_START.md`

---

*Last Updated: 2025*
*Architecture Version: 1.0*

