import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load raw env file to get the string exactly as is
with open(".env", "r") as f:
    for line in f:
        if line.startswith("DATABASE_URL="):
            database_url = line.strip().split("=", 1)[1]
            break
    else:
        print("DATABASE_URL not found in .env")
        exit(1)

try:
    # Manual parsing to handle @ in password
    # Format: mysql+pymysql://user:password@host:port/dbname
    
    prefix = "mysql+pymysql://"
    if not database_url.startswith(prefix):
        print("Invalid DATABASE_URL format")
        exit(1)
        
    rest = database_url[len(prefix):]
    
    # Split by / to separate dbname
    if "/" in rest:
        creds_host, db_name = rest.rsplit("/", 1)
        # Remove query params if any
        if "?" in db_name:
            db_name = db_name.split("?")[0]
    else:
        print("Could not parse database name")
        exit(1)
        
    # Split by @ to separate credentials from host
    # We use rsplit to split from the right, ensuring we get the host correctly
    # even if password has @
    if "@" in creds_host:
        creds, host_port = creds_host.rsplit("@", 1)
    else:
        print("Could not parse host")
        exit(1)
        
    # Split creds by : to get user and password
    if ":" in creds:
        user, password = creds.split(":", 1)
    else:
        print("Could not parse user/password")
        exit(1)

    # URL encode the password
    encoded_password = urllib.parse.quote_plus(password)
    
    # Reconstruct the URL
    # We use 'mysql' database to connect initially
    root_url = f"{prefix}{user}:{encoded_password}@{host_port}/mysql"
    
    print(f"Connecting to: {prefix}{user}:****@{host_port}/mysql")
    
    engine = create_engine(root_url)
    
    with engine.connect() as conn:
        # Check if DB exists first
        result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
        if result.fetchone():
            print(f"Database '{db_name}' already exists.")
        else:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created.")
            
except Exception as e:
    print(f"Error creating database: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
