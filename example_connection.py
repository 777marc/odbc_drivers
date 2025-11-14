"""
Example script to connect to DB2 database using SQLAlchemy
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
import os
import sys

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
    print(f"Attempting to connect to DB2 at {DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}...")
    engine = create_engine(connection_string, echo=True)
    
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM SYSIBM.SYSDUMMY1"))
        print("\n✓ Connection successful!")
        print(f"Result: {result.fetchone()}")
        
except ImportError as e:
    print(f"\n❌ Import Error: Required Python package is missing")
    print(f"Details: {e}")
    print("\nPlease ensure the following packages are installed:")
    print("  - ibm_db")
    print("  - ibm_db_sa")
    print("  - sqlalchemy")
    sys.exit(1)
    
except OperationalError as e:
    print(f"\n❌ ODBC Operational Error: Failed to connect to database")
    print(f"Details: {e}")
    print("\nPossible causes:")
    print("  1. ODBC driver not installed or configured correctly")
    print("  2. Database server is not running or unreachable")
    print("  3. Network connectivity issues")
    print("  4. Incorrect host, port, or database name")
    print("  5. Firewall blocking the connection")
    print("\nCheck your connection parameters:")
    print(f"  Host: {DB2_HOST}")
    print(f"  Port: {DB2_PORT}")
    print(f"  Database: {DB2_DATABASE}")
    sys.exit(1)
    
except DatabaseError as e:
    print(f"\n❌ Database Error: Authentication or database access failed")
    print(f"Details: {e}")
    print("\nPossible causes:")
    print("  1. Invalid username or password")
    print("  2. User doesn't have access to the database")
    print("  3. Database doesn't exist")
    print("  4. User account is locked or expired")
    print("\nCheck your credentials:")
    print(f"  Username: {DB2_USERNAME}")
    print(f"  Database: {DB2_DATABASE}")
    sys.exit(1)
    
except SQLAlchemyError as e:
    print(f"\n❌ SQLAlchemy Error: Database operation failed")
    print(f"Details: {e}")
    print("\nThis could be a SQL syntax error or database-specific issue")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Unexpected Error: {type(e).__name__}")
    print(f"Details: {e}")
    print("\nPlease check:")
    print("  1. ODBC driver installation (run validate_odbc.py)")
    print("  2. Environment variables are set correctly")
    print("  3. DB2 client libraries are accessible")
    sys.exit(1)

print("\n✓ All checks passed. Connection test completed successfully.")

