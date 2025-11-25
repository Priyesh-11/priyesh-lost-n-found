from sqlalchemy import create_engine, text
from app.core.config import settings
import sys

def verify_user_in_db():
    try:
        # Read the email to verify
        try:
            with open("last_registered_email.txt", "r") as f:
                email = f.read().strip()
        except FileNotFoundError:
            print("❌ No email file found. Run test_register_db.py first.")
            return

        print(f"Verifying user in database: {email}")
        
        # Connect to database
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id, email, username, full_name, is_verified FROM users WHERE email = :email"),
                {"email": email}
            )
            user = result.fetchone()
            
            if user:
                print("✅ User found in database!")
                print("-" * 40)
                print(f"ID: {user.id}")
                print(f"Email: {user.email}")
                print(f"Username: {user.username}")
                print(f"Full Name: {user.full_name}")
                print(f"Verified: {user.is_verified}")
                print("-" * 40)
            else:
                print("❌ User NOT found in database!")

    except Exception as e:
        print(f"❌ Database error: {str(e)}")

if __name__ == "__main__":
    verify_user_in_db()
