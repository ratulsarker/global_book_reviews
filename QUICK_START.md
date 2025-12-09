# 🚀 Quick Start Guide

## Prerequisites
✅ **Neo4j** database running (with dump file loaded)  
✅ **MySQL** database running (with SQL file imported)

## Steps to Run

### 1. Install Python Dependencies
```bash
cd Dashboard603
pip3 install -r requirements.txt --user
```

Or if you prefer a virtual environment:
```bash
cd Dashboard603
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### 2. Update Database Credentials
Edit `Dashboard603/config.py` and update:
- **Neo4j password**: Change `NEO4J_PASSWORD` to match your Neo4j instance
- **MySQL password**: Change `MYSQL_PASSWORD` to match your MySQL instance
- **Neo4j database name**: Check `neo4j_queries.py` line 14 - ensure the database name matches your loaded dump

**Important**: Also check `Dashboard603/neo4j_queries.py` line 14 - the database name should match your Neo4j database.

### 3. Verify Database Names Match
- **Neo4j**: The database name in `neo4j_queries.py` (line 14) should match your Neo4j database
- **MySQL**: The database name in `config.py` (line 10) should be `goodbooks` (or your actual database name)

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
Open your browser and go to: **http://localhost:8501**

---

## Troubleshooting

### Connection Errors
- **Neo4j**: Ensure Neo4j is running on `bolt://localhost:7687` and the database name matches
- **MySQL**: Ensure MySQL is running on `localhost` and the database `goodbooks` exists

### Import Errors
If you see module import errors, make sure all dependencies are installed:
```bash
pip3 install streamlit neo4j pandas pyvis sqlalchemy matplotlib pymysql --user
```

### Database Not Found
- Check that the Neo4j dump file has been loaded into your Neo4j instance
- Check that the MySQL SQL file has been imported and the database exists

