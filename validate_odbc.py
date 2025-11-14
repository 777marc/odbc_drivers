"""
Validation script to check ODBC driver installation
"""
import sys
import os

def validate_odbc():
    """Validate ODBC driver installation"""
    print("=" * 60)
    print("ODBC Driver Validation")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables:")
    ibm_db_home = os.getenv('IBM_DB_HOME')
    ld_library_path = os.getenv('LD_LIBRARY_PATH')
    print(f"   IBM_DB_HOME: {ibm_db_home}")
    print(f"   LD_LIBRARY_PATH: {ld_library_path}")
    
    if not ibm_db_home:
        print("   ❌ IBM_DB_HOME not set")
        return False
    else:
        print("   ✓ IBM_DB_HOME is set")
    
    # Check if driver files exist
    print("\n2. Checking driver files:")
    driver_path = f"{ibm_db_home}/lib/libdb2o.so"
    if os.path.exists(driver_path):
        print(f"   ✓ Driver found: {driver_path}")
    else:
        print(f"   ❌ Driver not found: {driver_path}")
        return False
    
    # Check ODBC configuration
    print("\n3. Checking ODBC configuration:")
    odbc_ini = "/etc/odbcinst.ini"
    if os.path.exists(odbc_ini):
        print(f"   ✓ ODBC config found: {odbc_ini}")
        with open(odbc_ini, 'r') as f:
            print("   Contents:")
            for line in f:
                print(f"      {line.rstrip()}")
    else:
        print(f"   ❌ ODBC config not found: {odbc_ini}")
        return False
    
    # Try importing Python ODBC libraries
    print("\n4. Checking Python ODBC libraries:")
    
    try:
        import pyodbc
        print(f"   ✓ pyodbc version: {pyodbc.version}")
        
        # List available drivers
        drivers = pyodbc.drivers()
        print(f"   Available ODBC drivers: {drivers}")
    except ImportError as e:
        print(f"   ❌ pyodbc import failed: {e}")
    
    try:
        import ibm_db
        print(f"   ✓ ibm_db imported successfully")
    except ImportError as e:
        print(f"   ❌ ibm_db import failed: {e}")
    
    try:
        import ibm_db_sa
        print(f"   ✓ ibm_db_sa imported successfully")
    except ImportError as e:
        print(f"   ❌ ibm_db_sa import failed: {e}")
    
    # Check SQLAlchemy
    print("\n5. Checking SQLAlchemy:")
    try:
        import sqlalchemy
        print(f"   ✓ SQLAlchemy version: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"   ❌ SQLAlchemy import failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ODBC validation completed successfully")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = validate_odbc()
    sys.exit(0 if success else 1)
