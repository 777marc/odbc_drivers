"""
Example script to connect to DB2 database using SQLAlchemy
"""
from sqlalchemy import create_engine, text
import os

# Connection parameters - use environment variables for security
DB2_HOST = os.getenv('DB2_HOST', 'localhost')
DB2_PORT = os.getenv('DB2_PORT', '50000')
DB2_DATABASE = os.getenv('DB2_DATABASE', 'sample')
DB2_USERNAME = os.getenv('DB2_USERNAME', 'db2inst1')
DB2_PASSWORD = os.getenv('DB2_PASSWORD', 'password')

# Method 1: Using ibm_db_sa driver (recommended for DB2)
connection_string = f"db2+ibm_db://{DB2_USERNAME}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}"

# Method 2: Using pyodbc driver (alternative)
# connection_string = f"db2+pyodbc://{DB2_USERNAME}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}?driver=DB2"

try:
    # Create engine
    engine = create_engine(connection_string, echo=True)
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM SYSIBM.SYSDUMMY1"))
        print("Connection successful!")
        print(f"Result: {result.fetchone()}")
        
except Exception as e:
    print(f"Connection failed: {e}")
