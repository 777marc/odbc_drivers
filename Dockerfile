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
    && rm -rf /var/lib/apt/lists/*

# Download and install IBM DB2 ODBC driver (clidriver v11.5.8)
RUN curl -O https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/v11.5.8_linuxx64_odbc_cli.tar.gz \
    && tar -xzf v11.5.8_linuxx64_odbc_cli.tar.gz -C /opt \
    && rm v11.5.8_linuxx64_odbc_cli.tar.gz

# Set environment variables for DB2 ODBC driver
ENV IBM_DB_HOME=/opt/clidriver
ENV LD_LIBRARY_PATH=${IBM_DB_HOME}/lib:${LD_LIBRARY_PATH}
ENV PATH=${IBM_DB_HOME}/bin:${PATH}

# Create ODBC configuration
RUN echo "[DB2]" > /etc/odbcinst.ini && \
    echo "Description = DB2 ODBC Driver" >> /etc/odbcinst.ini && \
    echo "Driver = ${IBM_DB_HOME}/lib/libdb2o.so" >> /etc/odbcinst.ini && \
    echo "FileUsage = 1" >> /etc/odbcinst.ini && \
    echo "DontDLClose = 1" >> /etc/odbcinst.ini

# Validate ODBC installation
RUN echo "Validating ODBC installation..." && \
    odbcinst -j && \
    ls -la ${IBM_DB_HOME}/lib/libdb2o.so && \
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

# Default command
CMD ["python"]
