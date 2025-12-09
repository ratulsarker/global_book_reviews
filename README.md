# 📚 Goodbooks Analytics Platform

Hybrid database dashboard using Neo4j (graph) and MySQL (relational).

## Setup

1. Install dependencies:
```bash
cd Dashboard603
pip3 install -r requirements.txt --user
```

2. Start Neo4j Desktop and load the dump file

3. Start MySQL and import the SQL file

4. Edit `Dashboard603/config.py` with your passwords

5. Run:
```bash
cd Dashboard603
python3 -m streamlit run app.py
```

Open: http://localhost:8501

## Features

- Neo4j: Graph analysis, recommendations, shortest paths
- MySQL: Analytics, trends, author statistics

## Data

- 10,000 books
- 6 million ratings
- 34,000+ tags
