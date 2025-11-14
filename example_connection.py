"""
Example script to connect to DB2 database using SQLAlchemy
"""
from sqlalchemy import create_engine, text, event, pool
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
from sqlalchemy.pool import QueuePool
import os
import sys
import time

# Connection parameters - use environment variables for security
DB2_HOST = os.getenv('DB2_HOST', 'localhost')
DB2_PORT = os.getenv('DB2_PORT', '50000')
DB2_DATABASE = os.getenv('DB2_DATABASE', 'sample')
DB2_USERNAME = os.getenv('DB2_USERNAME', 'db2inst1')
DB2_PASSWORD = os.getenv('DB2_PASSWORD', 'password')

# Timeout settings (in seconds) to prevent 504 gateway errors
CONNECTION_TIMEOUT = int(os.getenv('DB2_CONNECT_TIMEOUT', '30'))  # Connection timeout
QUERY_TIMEOUT = int(os.getenv('DB2_QUERY_TIMEOUT', '60'))  # Query execution timeout

# Connection pool settings to manage connections efficiently
POOL_SIZE = int(os.getenv('DB2_POOL_SIZE', '5'))  # Number of connections to maintain
MAX_OVERFLOW = int(os.getenv('DB2_MAX_OVERFLOW', '10'))  # Additional connections when pool is exhausted
POOL_RECYCLE = int(os.getenv('DB2_POOL_RECYCLE', '3600'))  # Recycle connections after 1 hour
POOL_PRE_PING = os.getenv('DB2_POOL_PRE_PING', 'true').lower() == 'true'  # Test connection before using

# Method 1: Using ibm_db_sa driver (recommended for DB2)
connection_string = f"db2+ibm_db://{DB2_USERNAME}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}"

# Add connection timeout to connection string
connection_string += f"?connecttimeout={CONNECTION_TIMEOUT}"

# Method 2: Using pyodbc driver (alternative)
# connection_string = f"db2+pyodbc://{DB2_USERNAME}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}?driver=DB2&timeout={CONNECTION_TIMEOUT}"


def execute_with_retry(connection, query, max_retries=3, retry_delay=2):
    """
    Execute a query with retry logic to handle transient failures
    
    Args:
        connection: Database connection
        query: SQL query to execute
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        Query result
    """
    for attempt in range(max_retries):
        try:
            result = connection.execute(query)
            return result
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Query failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                print(f"   Error: {e}")
                time.sleep(retry_delay)
            else:
                raise


try:
    # Create engine with connection pooling and timeout settings
    print(f"Attempting to connect to DB2 at {DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}...")
    print(f"Timeout settings: Connect={CONNECTION_TIMEOUT}s, Query={QUERY_TIMEOUT}s")
    
    engine = create_engine(
        connection_string,
        poolclass=QueuePool,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=POOL_PRE_PING,  # Verify connections before using
        echo=True,
        connect_args={
            'timeout': QUERY_TIMEOUT  # Query execution timeout
        }
    )
    
    # Add connection event listener to set statement timeout
    @event.listens_for(engine, "connect")
    def set_timeout(dbapi_conn, connection_record):
        """Set query timeout for each connection"""
        try:
            cursor = dbapi_conn.cursor()
            # Set statement timeout (DB2 specific)
            cursor.execute(f"SET CURRENT QUERY OPTIMIZATION = {QUERY_TIMEOUT}")
            cursor.close()
        except Exception as e:
            print(f"⚠️  Could not set query timeout: {e}")
    
    # Test connection with retry logic
    with engine.connect() as connection:
        print("\nExecuting test query...")
        result = execute_with_retry(
            connection,
            text("SELECT 1 FROM SYSIBM.SYSDUMMY1"),
            max_retries=3,
            retry_delay=2
        )
        print("\n✓ Connection successful!")
        print(f"Result: {result.fetchone()}")
        
        # Test connection keep-alive
        print("\nTesting connection keep-alive...")
        connection.execute(text("SELECT CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1"))
        print("✓ Keep-alive successful")

        
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

