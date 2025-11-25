from app.core.database import SessionLocal
from sqlalchemy import text

def fix_alembic_version():
    db = SessionLocal()
    try:
        # Check current version
        result = db.execute(text("SELECT version_num FROM alembic_version"))
        current_version = result.scalar()
        print(f"Current Alembic Version: {current_version}")
        
        # Reset to previous version
        previous_version = 'd4a0f45583cc'
        print(f"Resetting to: {previous_version}")
        
        db.execute(text(f"UPDATE alembic_version SET version_num = '{previous_version}'"))
        db.commit()
        
        print("Alembic version updated successfully.")
            
    except Exception as e:
        print(f"Error updating Alembic version: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_alembic_version()
