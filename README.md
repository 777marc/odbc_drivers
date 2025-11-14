# DB2 ODBC Driver with Python and SQLAlchemy

This Docker container provides Python 3.11 with IBM DB2 ODBC drivers (v11.5.8) and SQLAlchemy for database connectivity.

## Build the Docker Image

```bash
docker build -t python-db2-odbc:latest .
```

## Run the Container

### Interactive Mode

```bash
docker run -it --rm python-db2-odbc:latest bash
```

### Run with Environment Variables

```bash
docker run -it --rm \
  -e DB2_HOST=your_db2_host \
  -e DB2_PORT=50000 \
  -e DB2_DATABASE=your_database \
  -e DB2_USERNAME=your_username \
  -e DB2_PASSWORD=your_password \
  python-db2-odbc:latest python example_connection.py
```

### Using Docker Compose (optional)

Create a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  app:
    build: .
    environment:
      - DB2_HOST=your_db2_host
      - DB2_PORT=50000
      - DB2_DATABASE=your_database
      - DB2_USERNAME=your_username
      - DB2_PASSWORD=your_password
    volumes:
      - .:/app
```

## Connection String Examples

### Using ibm_db_sa (Recommended)

```python
connection_string = "db2+ibm_db://username:password@host:port/database"
```

### Using pyodbc

```python
connection_string = "db2+pyodbc://username:password@host:port/database?driver=DB2"
```

## Installed Packages

- SQLAlchemy >= 2.0.0
- ibm-db >= 3.2.0
- ibm-db-sa >= 0.4.0
- pyodbc >= 5.0.0

## ODBC Driver Location

- Driver Path: `/opt/clidriver/lib/libdb2o.so`
- Configuration: `/etc/odbcinst.ini`
