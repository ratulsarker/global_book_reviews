# 📚 Goodbooks Hybrid Dashboard

A comprehensive book analytics dashboard using **Neo4j** (graph database) and **MySQL** (relational database) with Streamlit.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Neo4j](https://img.shields.io/badge/neo4j-5.x-green.svg)
![MySQL](https://img.shields.io/badge/mysql-8.x-orange.svg)

## 🎯 Features

### Neo4j Graph Analytics
- 📚 Browse books by tags and ratings
- 🔍 Smart recommendations based on shared tags
- 🕸️ Interactive network graph visualizations
- 🛤️ Shortest path between books
- 📊 Centrality analysis (top authors and tags)
- 🔀 Graph traversal (related books)

### SQL Analytics
- 📊 Database overview and statistics
- 👥 Author analytics with visualizations
- 📈 Publication trends over time
- 🌍 Books by language distribution
- ⭐ Rating distribution analysis
- 🔍 Advanced book search

## 📁 Project Structure

```
project_603/
├── setup.sh                                    # 🚀 Run this first!
├── README.md                                   # You are here
├── Analytical SQL Queries.sql                  # SQL reference queries
├── goodbooks-2025-11-20T18-16-45.dump         # Neo4j database backup
└── Dashboard603/                               # Main application
    ├── .env.example                           # Configuration template
    ├── .env                                   # Your credentials (git-ignored)
    ├── app.py                                 # Streamlit dashboard
    ├── config.py                              # Database configuration
    ├── neo4j_queries.py                       # Neo4j Cypher queries
    ├── sql_queries.py                         # MySQL queries
    ├── graph_utils.py                         # Graph visualization
    ├── requirements.txt                       # Python dependencies
    ├── data/                                  # CSV source files
    │   ├── books.csv                          # 10,000 books
    │   ├── tags.csv                           # 34,000+ tags
    │   ├── book_tags.csv                      # Book-tag relationships
    │   ├── ratings.csv                        # 6 million ratings
    │   └── to_read.csv                        # To-read lists
    └── lib/                                   # JavaScript libraries
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Neo4j Desktop** or Neo4j Server
- **MySQL 8.0+** or compatible

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/goodbooks-dashboard.git
cd goodbooks-dashboard
```

2. **Run the setup script**

```bash
./setup.sh
```

This will:
- Install all Python dependencies
- Create configuration file from template

3. **Configure your credentials**

Edit `Dashboard603/.env`:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# MySQL Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DATABASE=goodbooks
```

4. **Set up Neo4j Database**

   a. Install [Neo4j Desktop](https://neo4j.com/download/)
   
   b. Create a new database named `goodbooks`
   
   c. **Stop** the database
   
   d. Restore from dump:
      - Click "..." → "Load database from file"
      - Select `goodbooks-2025-11-20T18-16-45.dump`
      - Choose database: `goodbooks`
   
   e. **Start** the database

5. **Set up MySQL Database**

   Option A: Import using MySQL command line:
   ```bash
   mysql -u root -p < Analytical\ SQL\ Queries.sql
   ```

   Option B: Use MySQL Workbench:
   - Open `Analytical SQL Queries.sql`
   - Execute all statements

6. **Run the Dashboard**

```bash
cd Dashboard603
./run.sh
```

Or use streamlit directly:
```bash
streamlit run app.py
```

The dashboard will automatically open at **http://localhost:8501**

## 📊 Dataset

- **Books**: 10,000 popular books from Goodreads
- **Users**: 53,000+ users
- **Ratings**: 6 million+ book ratings
- **Tags**: 34,000+ user-generated tags
- **Relationships**: 1 million+ book-tag connections

## 🔧 Configuration

All configuration is managed through environment variables in `Dashboard603/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j connection URI | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `adminadmin` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | - |
| `MYSQL_HOST` | MySQL host | `localhost` |
| `MYSQL_DATABASE` | MySQL database name | `goodbooks` |

## 🐛 Troubleshooting

### Neo4j Connection Issues

```bash
# Verify Neo4j is running
# Check Neo4j Desktop status or run:
systemctl status neo4j
```

### MySQL Connection Issues

```bash
# Check if MySQL is running
ps aux | grep mysql

# Test connection
mysql -u root -p -e "SHOW DATABASES;"
```

### Missing Dependencies

```bash
cd Dashboard603
pip install -r requirements.txt
```

## 📖 Usage Examples

### Finding Book Recommendations

1. Navigate to "Neo4j Insights" tab
2. Search for a book (e.g., "Harry Potter")
3. Click "Search Books"
4. Select a book from results
5. View recommendations and graph visualization

### Analyzing Publication Trends

1. Navigate to "SQL Insights" tab
2. Click "Trends" sub-tab
3. View publication trends over time
4. Explore language distribution charts

## 🤝 Contributing

This is a course project for MGTA603 - Database Systems. Feel free to fork and enhance!

## 📝 License

MIT License - feel free to use for educational purposes

## 👥 Authors

- Your Name - Neo4j Integration & Dashboard
- Teammate Name - SQL Queries & Analytics

## 🙏 Acknowledgments

- Dataset: [Goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k)
- Neo4j Community
- Streamlit Team

---

**Questions?** Open an issue or check the documentation in the code!
