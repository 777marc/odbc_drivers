# DB2 ODBC Driver with Python Flask API

This project provides a Python 3.11 Flask application with IBM DB2 ODBC drivers (v11.5.8) and SQLAlchemy for database connectivity. The application includes a REST API for checking database connection status.

## Features

- Python 3.11 slim Docker container
- IBM DB2 ODBC CLI driver v11.5.8
- Flask REST API running on port 3030
- SQLAlchemy with connection pooling
- Timeout and retry mechanisms to prevent 504 gateway errors
- Comprehensive error handling for ODBC connection issues
- Health check and database status endpoints

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Service health check
- `GET /dbstatus` - Database connection status with detailed diagnostics

## Quick Start

### Using Docker Compose (Recommended)

1. Create a `.env` file (see `.env.example` for reference):

```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials:

```env
DB2_HOST=your_db2_host
DB2_PORT=50000
DB2_DATABASE=your_database
DB2_USERNAME=your_username
DB2_PASSWORD=your_password
```

3. Start the application:

```bash
docker-compose up
```

4. Access the API:

```bash
# Check health
curl http://localhost:3030/health

# Check database status
curl http://localhost:3030/dbstatus
```

### Using Docker

1. Build the Docker image:

```bash
docker build -t python-db2-odbc:latest .
```

2. Run the container:

```bash
docker run -p 3030:3030 \
  -e DB2_HOST=your_db2_host \
  -e DB2_PORT=50000 \
  -e DB2_DATABASE=your_database \
  -e DB2_USERNAME=your_username \
  -e DB2_PASSWORD=your_password \
  python-db2-odbc:latest
```

### Local Development

1. Set up Python virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate      # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables and run:

```bash
$env:DB2_HOST="localhost"
$env:DB2_PORT="50000"
$env:DB2_DATABASE="sample"
$env:DB2_USERNAME="db2inst1"
$env:DB2_PASSWORD="password"

python app.py
```

## Configuration

### Environment Variables

#### Database Connection

- `DB2_HOST` - Database host (default: localhost)
- `DB2_PORT` - Database port (default: 50000)
- `DB2_DATABASE` - Database name (default: sample)
- `DB2_USERNAME` - Database username (default: db2inst1)
- `DB2_PASSWORD` - Database password (default: password)

#### Timeout Settings (Prevent 504 Gateway Errors)

- `DB2_CONNECT_TIMEOUT` - Connection timeout in seconds (default: 30)
- `DB2_QUERY_TIMEOUT` - Query execution timeout in seconds (default: 60)

#### Connection Pool Settings

- `DB2_POOL_SIZE` - Number of persistent connections (default: 5)
- `DB2_MAX_OVERFLOW` - Additional connections when pool exhausted (default: 10)
- `DB2_POOL_RECYCLE` - Recycle connections after N seconds (default: 3600)
- `DB2_POOL_PRE_PING` - Test connections before using (default: true)

## Project Structure

```
.
├── app.py                  # Flask application with REST API
├── validate_odbc.py        # ODBC driver validation script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── .env.example          # Environment variables template
├── .dockerignore         # Docker build exclusions
└── driver/               # DB2 ODBC driver files (add manually)
    └── linuxx64_odbc_cli_11.5.tar.gz
```

## Installed Packages

- Flask >= 3.0.0
- SQLAlchemy >= 2.0.0
- ibm-db >= 3.2.0
- ibm-db-sa >= 0.4.0
- pyodbc >= 5.0.0

## ODBC Driver Information

- **Driver Path**: `/opt/ibm/clidriver/lib/libdb2.so`
- **Configuration**: `/etc/odbcinst.ini`
- **Version**: IBM DB2 ODBC CLI Driver v11.5.8

## Validation

To validate the ODBC driver installation inside the container:

```bash
docker-compose run --rm python-db2-app python validate_odbc.py
```

Or in an interactive shell:

```bash
docker-compose run --rm python-db2-app bash
python validate_odbc.py
```

## Troubleshooting

### 504 Gateway Timeout Errors

- Adjust `DB2_CONNECT_TIMEOUT` and `DB2_QUERY_TIMEOUT` values
- Check network connectivity to DB2 server
- Verify firewall rules allow connections

### ODBC Driver Issues

- Run `validate_odbc.py` to check installation
- Verify driver files exist in `/opt/ibm/clidriver/lib/`
- Check `LD_LIBRARY_PATH` includes driver directory

### Connection Failures

- Verify database credentials are correct
- Ensure DB2 server is running and accessible
- Check database name, host, and port configuration
- Review logs: `docker-compose logs -f`

## API Response Examples

### Health Check

```json
{
  "status": "healthy",
  "service": "db2-flask-app"
}
```

### Database Status (Success)

```json
{
  "status": "connected",
  "database": "sample",
  "host": "localhost",
  "port": "50000",
  "timestamp": "2025-11-15 10:30:45.123456",
  "message": "Database connection successful"
}
```

### Database Status (Error)

```json
{
  "status": "error",
  "error_type": "OperationalError",
  "message": "Failed to connect to database",
  "details": "Connection timeout...",
  "database": "sample",
  "host": "localhost",
  "port": "50000"
}
```

## License

This project uses IBM DB2 ODBC drivers which require acceptance of IBM's license terms.
