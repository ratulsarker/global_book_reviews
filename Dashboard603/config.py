# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "adminadmin"  # Change this to your Neo4j password

# MySQL Configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "ratul2468"  # Change this to your MySQL password
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "goodbooks"

SQL_CONNECTION_STRING = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
