"""
Quick script to add demo data to production database
Uses direct database connection to Railway
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.models.item import Item, Category
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

# Your Railway database URL
DATABASE_URL = "mysql+pymysql://root:cjInEvuWwKsSyoCAGGYIcLAygJSxacSY@maglev.proxy.rlwy.net:39846/railway"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def create_demo_users():
    """Create demo users including admin"""
    print("Creating demo users...")
    
    users_data = [
        {
            "email": "admin@test.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "is_admin": True,
            "is_verified": True
        },
        {
            "email": "priyesh@test.com",
            "username": "priyesh",
            "password": "priyesh123",
            "full_name": "Priyesh Singh",
            "phone": "+91 9876543210",
            "is_verified": True
        },
        {
            "email": "user1@test.com",
            "username": "user1",
            "password": "user123",
            "full_name": "Test User",
            "is_verified": True
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Check if user exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"  ⚠️  User {user_data['username']} already exists, skipping...")
            created_users.append(existing)
            continue
        
        # Hash password
        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        
        # Create user
        user = User(
            **user_data,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        created_users.append(user)
        print(f"  ✅ Created user: {user.username}")
    
    return created_users

def create_demo_items(users):
    """Create demo lost and found items"""
    print("\nCreating demo items...")
    
    # Get some categories
    categories = db.query(Category).all()
    if not categories:
        print("  ⚠️  No categories found! Run migrations first.")
        return
    
    cat_dict = {cat.name.lower(): cat.id for cat in categories}
    
    items_data = [
        {
            "title": "Blue Backpack",
            "description": "Blue JanSport backpack with laptop inside. Lost near the library. Has my name tag inside.",
            "type": "lost",
            "category_id": cat_dict.get("bag", 1),
            "location": "Library",
            "date_lost": datetime.now() - timedelta(days=2),
            "status": "active"
        },
        {
            "title": "iPhone 13 Pro",
            "description": "Black iPhone 13 Pro in blue protective case. Found on bench.",
            "type": "found",
            "category_id": cat_dict.get("electronics", 1),
            "location": "Cafeteria",
            "date_found": datetime.now() - timedelta(days=1),
            "status": "active"
        },
        {
            "title": "Car Keys - Toyota",
            "description": "Toyota car keys with red keychain. Has remote.",
            "type": "found",
            "category_id": cat_dict.get("keys", 1),
            "location": "Parking Lot",
            "date_found": datetime.now() - timedelta(hours=5),
            "status": "active"
        },
        {
            "title": "Brown Leather Wallet",
            "description": "Brown leather wallet, contains student ID card and some cash.",
            "type": "lost",
            "category_id": cat_dict.get("wallet", 1),
            "location": "Sports Complex",
            "date_lost": datetime.now() - timedelta(days=3),
            "status": "active"
        },
        {
            "title": "Gold Watch",
            "description": "Men's gold wristwatch, possibly Casio brand.",
            "type": "found",
            "category_id": cat_dict.get("jewelry", 1) or cat_dict.get("other", 1),
            "location": "Gym",
            "date_found": datetime.now() - timedelta(hours=12),
            "status": "active"
        },
        {
            "title": "Student ID Card",
            "description": "Student ID card belonging to John Smith.",
            "type": "found",
            "category_id": cat_dict.get("documents", 1) or cat_dict.get("other", 1),
            "location": "Main Gate",
            "date_found": datetime.now() - timedelta(hours=3),
            "status": "active"
        }
    ]
    
    for i, item_data in enumerate(items_data):
        # Assign to random user
        user = random.choice(users)
        item_data["user_id"] = user.id
        
        item = Item(**item_data)
        db.add(item)
        print(f"  ✅ Created {item_data['type']} item: {item_data['title']}")
    
    db.commit()

def main():
    print("=" * 60)
    print("POPULATING RAILWAY PRODUCTION DATABASE")
    print("=" * 60)
    
    try:
        # Create users
        users = create_demo_users()
        
        # Create items
        create_demo_items(users)
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Your database now has demo data!")
        print("=" * 60)
        print("\n🔑 Demo Credentials:")
        print("   Admin: admin@test.com / admin123")
        print("   User:  priyesh@test.com / priyesh123")
        print("   User:  user1@test.com / user123")
        print("\n🌐 Visit: https://lost-found-pri.vercel.app")
        print("   (After you update the Vercel env variable and redeploy)")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
