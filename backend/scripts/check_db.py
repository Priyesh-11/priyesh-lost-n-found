from app.core.database import SessionLocal
from sqlalchemy import text

def check_tables():
    db = SessionLocal()
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        print("Tables in database:", tables)
        
        if 'claims' in tables:
            print("Claims table exists.")
            # Check columns
            result = db.execute(text("DESCRIBE claims"))
            columns = [row[0] for row in result]
            print("Columns in claims table:", columns)
        else:
            print("Claims table MISSING!")
            
    except Exception as e:
        print(f"Error checking DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_tables()
