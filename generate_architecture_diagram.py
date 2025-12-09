#!/usr/bin/env python3
"""
Generate System Architecture Diagram for Goodbooks Analytics Platform
Creates a visual representation of the hybrid database architecture.
"""

try:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.onprem.database import MySQL, Neo4j
    from diagrams.onprem.client import Users
    from diagrams.programming.language import Python
    from diagrams.onprem.web import Streamlit
    from diagrams.onprem.analytics import Spark
    from diagrams.onprem.inmemory import Redis
    from diagrams.programming.flowchart import Database
    HAS_DIAGRAMS = True
except ImportError:
    HAS_DIAGRAMS = False
    print("⚠️  'diagrams' library not installed. Installing...")
    import subprocess
    subprocess.run(["pip3", "install", "diagrams", "--user"], check=False)
    print("✅ Please run this script again after installation completes.")

if HAS_DIAGRAMS:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.onprem.database import MySQL, Neo4j
    from diagrams.onprem.client import Users
    from diagrams.programming.language import Python
    from diagrams.onprem.web import Streamlit

def create_architecture_diagram():
    """Generate the system architecture diagram."""
    
    with Diagram("Goodbooks Analytics Platform - System Architecture", 
                 filename="system_architecture", 
                 show=False,
                 direction="TB",
                 outformat="png"):
        
        # User Layer
        users = Users("End Users\n(Browser)")
        
        # Application Layer
        with Cluster("Application Layer"):
            dashboard = Streamlit("Streamlit Dashboard\n(Python Web App)\nhttp://localhost:8501")
            app_code = Python("app.py\nconfig.py\nneo4j_queries.py\nsql_queries.py")
            dashboard >> app_code
        
        # Database Layer
        with Cluster("Database Layer (Must Run Before Dashboard)"):
            mysql = MySQL("MySQL Database\n(Relational)\nPort: 3306\nDB: goodbooks\n\n• 10,000 books\n• 6M ratings\n• Structured analytics\n• JOINs & Aggregations")
            
            neo4j = Neo4j("Neo4j Database\n(Graph)\nPort: 7687\nDB: goodbooks-2025-...\n\n• Graph relationships\n• Recommendations\n• Shortest paths\n• Network analysis")
        
        # Data Layer
        with Cluster("Data Sources"):
            csv_files = Database("CSV Files\n\n• books.csv\n• tags.csv\n• book_tags.csv\n• ratings.csv\n• to_read.csv")
        
        # Connections
        users >> Edge(label="HTTP Requests", color="blue") >> dashboard
        dashboard >> Edge(label="SQL Queries\n(SQLAlchemy + PyMySQL)", color="green") >> mysql
        dashboard >> Edge(label="Cypher Queries\n(Neo4j Python Driver)", color="purple") >> neo4j
        csv_files >> Edge(label="Data Import", color="orange", style="dashed") >> mysql
        csv_files >> Edge(label="Data Import", color="orange", style="dashed") >> neo4j

if __name__ == "__main__":
    if HAS_DIAGRAMS:
        print("🎨 Generating architecture diagram...")
        create_architecture_diagram()
        print("✅ Diagram saved as 'system_architecture.png'")
        print("📊 Diagram saved as 'system_architecture.png'")
    else:
        print("❌ Please install diagrams library first:")
        print("   pip3 install diagrams --user")

