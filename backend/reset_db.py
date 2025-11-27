from app.core.database import Base, engine
from app.models import user, item, claim, role, activity, report, item_image
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped.")
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
    
    print("Database reset successfully.")

if __name__ == "__main__":
    reset_db()
