# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required for ODBC and DB2
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    libxml2 \
    libpam0g \
    libstdc++6 \
    ksh \
    odbcinst \
    && rm -rf /var/lib/apt/lists/*

# Install IBM DB2 ODBC driver (clidriver v11.5.8)
COPY ./driver/linuxx64_odbc_cli_11.5.tar.gz /tmp/linuxx64_odbc_cli.tar.gz
RUN if [ -f /tmp/linuxx64_odbc_cli.tar.gz ]; then \
      mkdir -p /opt/ibm/clidriver && \
      tar -xzf /tmp/linuxx64_odbc_cli.tar.gz -C /opt/ibm/clidriver --strip-components=1 && \
      rm /tmp/linuxx64_odbc_cli.tar.gz && \
      echo "clidriver extracted to /opt/ibm/clidriver"; \
    else \
      echo "No local clidriver tarball found at driver/linuxx64_odbc_cli.tar.gz"; \
    fi

# Set environment variables for DB2 ODBC driver
ENV IBM_DB_HOME=/opt/ibm/clidriver
ENV LD_LIBRARY_PATH=${IBM_DB_HOME}/lib:${LD_LIBRARY_PATH}
ENV PATH=${IBM_DB_HOME}/bin:${PATH}

# Create ODBC configuration
RUN echo "[DB2]" > /etc/odbcinst.ini && \
    echo "Description = DB2 ODBC Driver" >> /etc/odbcinst.ini && \
    echo "Driver = ${IBM_DB_HOME}/lib/libdb2.so" >> /etc/odbcinst.ini && \
    echo "FileUsage = 1" >> /etc/odbcinst.ini && \
    echo "DontDLClose = 1" >> /etc/odbcinst.ini

# Validate ODBC installation
RUN echo "Validating ODBC installation..." && \
    odbcinst -j && \
    ls -la ${IBM_DB_HOME}/lib/libdb2.so && \
    ${IBM_DB_HOME}/bin/db2level && \
    echo "ODBC installation validated successfully"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 3030
EXPOSE 3030

# Default command
CMD ["python", "app.py"]
