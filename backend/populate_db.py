import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.role import Role
from app.models.item import Item, ItemType, ItemStatus, Category
from app.models.claim import Claim, ClaimStatus
from app.models.report import Report
from app.models.item_image import ItemImage
from app.models.activity import UserActivity
from app.core.security import get_password_hash

def populate():
    db = SessionLocal()
    try:
        # Create Roles
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(name="admin", permissions={"all": True})
            db.add(admin_role)
        
        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            user_role = Role(name="user", permissions={"read": True, "write": True})
            db.add(user_role)
        
        db.commit()
        db.refresh(admin_role)
        db.refresh(user_role)

        # Create Categories
        categories = ["Electronics", "Wallet", "Keys", "Bag", "Jewelry", "Documents", "Pets", "Other"]
        cat_map = {}
        for cat_name in categories:
            cat = db.query(Category).filter(Category.name == cat_name).first()
            if not cat:
                cat = Category(name=cat_name, icon=cat_name.lower())
                db.add(cat)
            cat_map[cat_name] = cat
        
        db.commit()
        # Refresh categories to get IDs
        for name, cat in cat_map.items():
             db.refresh(cat)

        # Create Users
        users = []
        # Admin
        admin = db.query(User).filter((User.email == "admin@example.com") | (User.username == "admin")).first()
        if not admin:
            admin = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role_id=admin_role.id,
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            users.append(admin)
        else:
            users.append(admin)
        
        # Regular User 1
        user1 = db.query(User).filter((User.email == "john@example.com") | (User.username == "johndoe")).first()
        if not user1:
            user1 = User(
                email="john@example.com",
                username="johndoe",
                hashed_password=get_password_hash("password123"),
                full_name="John Doe",
                role_id=user_role.id,
                is_active=True,
                is_verified=True
            )
            db.add(user1)
            users.append(user1)
        else:
            users.append(user1)

        # Regular User 2
        user2 = db.query(User).filter((User.email == "jane@example.com") | (User.username == "janedoe")).first()
        if not user2:
            user2 = User(
                email="jane@example.com",
                username="janedoe",
                hashed_password=get_password_hash("password123"),
                full_name="Jane Doe",
                role_id=user_role.id,
                is_active=True,
                is_verified=True
            )
            db.add(user2)
            users.append(user2)
        else:
            users.append(user2)
        
        db.commit()
        
        # Re-query users to ensure we have objects
        user1 = db.query(User).filter(User.username == "johndoe").first()
        user2 = db.query(User).filter(User.username == "janedoe").first()
        
        # Create Items
        items_data = [
            {
                "title": "Lost iPhone 13",
                "description": "Black iPhone 13 with a clear case. Lost near Central Park.",
                "type": ItemType.LOST,
                "status": ItemStatus.ACTIVE,
                "location": "Central Park, NY",
                "category": cat_map["Electronics"],
                "user": user1,
                "date_lost": datetime.now() - timedelta(days=2)
            },
            {
                "title": "Found Brown Leather Wallet",
                "description": "Brown leather wallet found on the subway. Contains some cash and cards.",
                "type": ItemType.FOUND,
                "status": ItemStatus.ACTIVE,
                "location": "Subway Station, NY",
                "category": cat_map["Wallet"],
                "user": user2,
                "date_lost": datetime.now() - timedelta(days=1)
            },
             {
                "title": "Lost Car Keys",
                "description": "Toyota car keys with a red keychain.",
                "type": ItemType.LOST,
                "status": ItemStatus.ACTIVE,
                "location": "Shopping Mall",
                "category": cat_map["Keys"],
                "user": user1,
                "date_lost": datetime.now() - timedelta(days=5)
            },
             {
                "title": "Found Blue Backpack",
                "description": "Blue Nike backpack found in the library.",
                "type": ItemType.FOUND,
                "status": ItemStatus.ACTIVE,
                "location": "City Library",
                "category": cat_map["Bag"],
                "user": user2,
                "date_lost": datetime.now() - timedelta(hours=5)
            }
        ]

        for item_data in items_data:
            # Check if item exists (simple check by title)
            existing = db.query(Item).filter(Item.title == item_data["title"]).first()
            if not existing:
                item = Item(
                    title=item_data["title"],
                    description=item_data["description"],
                    type=item_data["type"],
                    status=item_data["status"],
                    location=item_data["location"],
                    category_id=item_data["category"].id,
                    user_id=item_data["user"].id,
                    date_lost=item_data["date_lost"],
                    contact_method="email",
                    is_approved=True
                )
                db.add(item)
                db.flush() # Flush to get ID
                
                # Add a fake claim for the found item
                if item.type == ItemType.FOUND and item.title == "Found Brown Leather Wallet":
                    claim = Claim(
                        item_id=item.id,
                        claimant_id=user1.id, # User1 claims User2's found item
                        status=ClaimStatus.PENDING,
                        proof_description="I lost a brown wallet with my ID in it.",
                        proof_image_url="https://via.placeholder.com/150"
                    )
                    db.add(claim)
        
        db.commit()
        print("Database populated successfully!")

    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate()
