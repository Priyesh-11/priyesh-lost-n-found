import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime

# Add the current directory to sys.path to allow importing app modules
sys.path.append(os.getcwd())

from app.core.config import settings
from app.models.user import User
from app.models.role import Role
from app.models.item import Item, Category, ItemType, ItemStatus
from app.models.item_image import ItemImage

# Setup database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Setup password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_data():
    print("Starting database seeding...")

    # 1. Create Roles
    print("Creating roles...")
    roles = ["user", "admin"]
    role_map = {}
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_map[role_name] = role.id
    
    # 2. Create Users
    print("Creating users...")
    mock_users = [
      {
        "id": '1',
        "email": 'john.doe@example.com',
        "username": 'johndoe',
        "fullName": 'John Doe',
        "phone": '+1234567890',
        "role": 'user',
        "reputation": 85,
        "isVerified": True,
      },
      {
        "id": '2',
        "email": 'admin@lostandfound.com',
        "username": 'admin',
        "fullName": 'Admin User',
        "phone": '+1234567891',
        "role": 'admin',
        "reputation": 100,
        "isVerified": True,
      }
    ]

    user_map = {} # Map mock ID to real DB ID
    
    for u_data in mock_users:
        user = db.query(User).filter(User.email == u_data["email"]).first()
        if not user:
            user = User(
                email=u_data["email"],
                username=u_data["username"],
                full_name=u_data["fullName"],
                phone=u_data["phone"],
                hashed_password=get_password_hash("password123"),
                role_id=role_map[u_data["role"]],
                is_verified=u_data["isVerified"],
                reputation_score=u_data["reputation"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        user_map[u_data["id"]] = user.id

    # 3. Create Categories
    print("Creating categories...")
    mock_categories = [
        {'value': 'electronics', 'label': 'Electronics'},
        {'value': 'wallet', 'label': 'Wallets'},
        {'value': 'keys', 'label': 'Keys'},
        {'value': 'bag', 'label': 'Bags'},
        {'value': 'jewelry', 'label': 'Jewelry'},
        {'value': 'documents', 'label': 'Documents'},
        {'value': 'pets', 'label': 'Pets'},
        {'value': 'other', 'label': 'Other'}
    ]
    
    category_map = {}
    for cat_data in mock_categories:
        cat = db.query(Category).filter(Category.name == cat_data["value"]).first()
        if not cat:
            cat = Category(name=cat_data["value"]) # Using value as name for simplicity
            db.add(cat)
            db.commit()
            db.refresh(cat)
        category_map[cat_data["value"]] = cat.id

    # 4. Create Items
    print("Creating items...")
    mock_items = [
      {
        "title": 'Black Leather Wallet',
        "description": 'Lost black leather wallet near Central Park. Contains ID cards and credit cards. Very important to me. Reward offered for return.',
        "category": 'wallet',
        "type": 'lost',
        "status": 'active',
        "location": 'Central Park, New York',
        "date": '2024-03-15T14:30:00Z',
        "images": ['https://images.unsplash.com/photo-1579014134953-1580d7f123f3'],
        "userId": '1',
      },
      {
        "title": 'Found Set of House Keys',
        "description": 'Found a set of house keys with a blue keychain near the subway station on Main Street. Keys appear to be for a house or apartment.',
        "category": 'keys',
        "type": 'found',
        "status": 'active',
        "location": 'Main Street Subway Station',
        "date": '2024-03-18T09:15:00Z',
        "images": ['https://images.unsplash.com/flagged/photo-1564767609342-620cb19b2357'],
        "userId": '1',
      },
      {
        "title": 'iPhone 14 Pro',
        "description": 'Lost my iPhone 14 Pro with a black case at the coffee shop on 5th Avenue. Has a small crack on the screen. Please contact if found.',
        "category": 'electronics',
        "type": 'lost',
        "status": 'active',
        "location": '5th Avenue Coffee Shop',
        "date": '2024-03-20T16:45:00Z',
        "images": ['https://images.unsplash.com/photo-1511707171634-5f897ff02aa9'],
        "userId": '1',
      },
      {
        "title": 'Red Leather Handbag',
        "description": 'Found a beautiful red leather handbag at the bus stop near the library. Contains some personal items. Looking for the owner.',
        "category": 'bag',
        "type": 'found',
        "status": 'active',
        "location": 'Library Bus Stop',
        "date": '2024-03-19T11:20:00Z',
        "images": ['https://images.unsplash.com/photo-1584917865442-de89df76afd3'],
        "userId": '1',
      },
      {
        "title": 'Brown Wallet with Cash',
        "description": 'Found a brown wallet containing some cash and cards near the park entrance. Trying to find the rightful owner.',
        "category": 'wallet',
        "type": 'found',
        "status": 'active',
        "location": 'City Park Entrance',
        "date": '2024-03-21T08:30:00Z',
        "images": ['https://images.unsplash.com/photo-1512358958014-b651a7ee1773'],
        "userId": '1',
      },
      {
        "title": 'Vintage Keys Collection',
        "description": 'Lost a collection of vintage skeleton keys that have sentimental value. Last seen near the antique shop.',
        "category": 'keys',
        "type": 'lost',
        "status": 'active',
        "location": 'Antique Shop, Downtown',
        "date": '2024-03-17T13:00:00Z',
        "images": ['https://images.unsplash.com/photo-1609587415882-97552f39c6c2'],
        "userId": '1',
      },
      {
        "title": 'iPhone on Table',
        "description": 'Found an iPhone left on a table at the restaurant. Screen is unlocked. Please claim if this is yours.',
        "category": 'electronics',
        "type": 'found',
        "status": 'active',
        "location": 'Downtown Restaurant',
        "date": '2024-03-22T19:30:00Z',
        "images": ['https://images.unsplash.com/photo-1580910051074-3eb694886505'],
        "userId": '1',
      },
      {
        "title": 'Black Tote Bag',
        "description": 'Lost my black tote bag with laptop inside at the train station. Very important work documents. Urgent!',
        "category": 'bag',
        "type": 'lost',
        "status": 'active',
        "location": 'Central Train Station',
        "date": '2024-03-23T07:45:00Z',
        "images": ['https://images.unsplash.com/photo-1614179689702-355944cd0918'],
        "userId": '1',
      }
    ]

    for item_data in mock_items:
        # Check if item exists (by title and user)
        existing_item = db.query(Item).filter(Item.title == item_data["title"]).first()
        if not existing_item:
            # Parse date
            try:
                date_lost = datetime.fromisoformat(item_data["date"].replace("Z", "+00:00"))
            except:
                date_lost = datetime.now()

            item = Item(
                title=item_data["title"],
                description=item_data["description"],
                category_id=category_map[item_data["category"]],
                type=ItemType(item_data["type"]),
                status=ItemStatus(item_data["status"]),
                location=item_data["location"],
                date_lost=date_lost,
                user_id=user_map[item_data["userId"]],
                contact_method="email", # Default
                is_approved=True
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            
            # Add images
            for img_url in item_data["images"]:
                image = ItemImage(
                    item_id=item.id,
                    image_url=img_url,
                    is_primary=True # First one is primary
                )
                db.add(image)
            db.commit()

    print("Database seeding completed successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()
