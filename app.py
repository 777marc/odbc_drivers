"""
Flask application with DB2 database status endpoint
"""
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
import os

app = Flask(__name__)

# Database connection parameters
DB2_HOST = os.getenv('DB2_HOST', 'localhost')
DB2_PORT = os.getenv('DB2_PORT', '50000')
DB2_DATABASE = os.getenv('DB2_DATABASE', 'sample')
DB2_USERNAME = os.getenv('DB2_USERNAME', 'db2inst1')
DB2_PASSWORD = os.getenv('DB2_PASSWORD', 'password')

# Timeout settings
CONNECTION_TIMEOUT = int(os.getenv('DB2_CONNECT_TIMEOUT', '30'))
QUERY_TIMEOUT = int(os.getenv('DB2_QUERY_TIMEOUT', '60'))

# Connection pool settings
POOL_SIZE = int(os.getenv('DB2_POOL_SIZE', '5'))
MAX_OVERFLOW = int(os.getenv('DB2_MAX_OVERFLOW', '10'))
POOL_RECYCLE = int(os.getenv('DB2_POOL_RECYCLE', '3600'))
POOL_PRE_PING = os.getenv('DB2_POOL_PRE_PING', 'true').lower() == 'true'

# Create connection string
connection_string = f"db2+ibm_db://{DB2_USERNAME}:{DB2_PASSWORD}@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}?connecttimeout={CONNECTION_TIMEOUT}"

# Create SQLAlchemy engine
engine = create_engine(
    connection_string,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=POOL_PRE_PING
)


@app.route('/dbstatus', methods=['GET'])
def db_status():
    """
    Check database connection status
    Returns JSON with connection status and details
    """
    try:
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1"))
            timestamp = result.fetchone()[0]
            
            return jsonify({
                'status': 'connected',
                'database': DB2_DATABASE,
                'host': DB2_HOST,
                'port': DB2_PORT,
                'timestamp': str(timestamp),
                'message': 'Database connection successful'
            }), 200
            
    except OperationalError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'OperationalError',
            'message': 'Failed to connect to database',
            'details': str(e),
            'database': DB2_DATABASE,
            'host': DB2_HOST,
            'port': DB2_PORT
        }), 503
        
    except DatabaseError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'DatabaseError',
            'message': 'Database authentication or access error',
            'details': str(e),
            'database': DB2_DATABASE,
            'host': DB2_HOST
        }), 503
        
    except SQLAlchemyError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'SQLAlchemyError',
            'message': 'Database operation failed',
            'details': str(e)
        }), 503
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error_type': type(e).__name__,
            'message': 'Unexpected error occurred',
            'details': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'db2-flask-app'
    }), 200


@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users from the users table
    Returns JSON array of all users
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users"))
            
            # Get column names
            columns = list(result.keys())
            
            # Convert rows to list of dictionaries
            users = []
            for row in result:
                user = {columns[i]: row[i] for i in range(len(columns))}
                users.append(user)
            
            return jsonify({
                'status': 'success',
                'count': len(users),
                'users': users
            }), 200
            
    except OperationalError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'OperationalError',
            'message': 'Failed to connect to database',
            'details': str(e)
        }), 503
        
    except DatabaseError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'DatabaseError',
            'message': 'Database query error - table may not exist',
            'details': str(e)
        }), 404
        
    except SQLAlchemyError as e:
        return jsonify({
            'status': 'error',
            'error_type': 'SQLAlchemyError',
            'message': 'Database operation failed',
            'details': str(e)
        }), 500
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error_type': type(e).__name__,
            'message': 'Unexpected error occurred',
            'details': str(e)
        }), 500


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API information
    """
    return jsonify({
        'service': 'DB2 Flask Application',
        'endpoints': {
            '/': 'API information',
            '/health': 'Health check',
            '/dbstatus': 'Database connection status',
            '/users': 'Get all users from users table'
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)
