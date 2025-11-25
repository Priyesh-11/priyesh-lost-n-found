"""
Script to populate production database with test data
Run this locally - it will connect to your production Railway database
"""
import requests
import json

# Your production backend URL
BACKEND_URL = "https://priyesh-lost-n-found-backend.onrender.com/api/v1"

def create_test_users():
    """Create test users including admin"""
    
    users = [
        {
            "email": "admin@test.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "is_admin": True
        },
        {
            "email": "priyesh@test.com",
            "username": "priyesh",
            "password": "priyesh123",
            "full_name": "Priyesh Singh",
            "phone": "+91 9876543210"
        },
        {
            "email": "user1@test.com",
            "username": "user1",
            "password": "user123",
            "full_name": "Test User 1"
        }
    ]
    
    print("Creating test users...")
    created_users = []
    
    for user_data in users:
        try:
            # Remove is_admin from payload (not in schema)
            is_admin = user_data.pop("is_admin", False)
            
            response = requests.post(
                f"{BACKEND_URL}/auth/register",
                json=user_data
            )
            
            if response.status_code == 200:
                print(f"✅ Created user: {user_data['username']}")
                created_users.append(response.json())
            else:
                print(f"❌ Failed to create {user_data['username']}: {response.text}")
        except Exception as e:
            print(f"❌ Error creating {user_data['username']}: {str(e)}")
    
    return created_users

def create_test_items(token):
    """Create sample lost and found items"""
    
    items = [
        {
            "title": "Blue Backpack",
            "description": "Blue JanSport backpack with laptop inside. Lost near the library.",
            "type": "lost",
            "category_id": 4,  # Bag
            "location": "Library",
            "date_lost": "2025-11-24T10:00:00"
        },
        {
            "title": "iPhone 13 Pro",
            "description": "Black iPhone 13 Pro in blue case",
            "type": "found",
            "category_id": 1,  # Electronics
            "location": "Cafeteria",
            "date_found": "2025-11-25T14:30:00"
        },
        {
            "title": "Car Keys",
            "description": "Toyota car keys with red keychain",
            "type": "found",
            "category_id": 3,  # Keys
            "location": "Parking Lot",
            "date_found": "2025-11-25T09:00:00"
        },
        {
            "title": "Wallet",
            "description": "Brown leather wallet, contains student ID",
            "type": "lost",
            "category_id": 2,  # Wallet
            "location": "Sports Complex",
            "date_lost": "2025-11-23T16:00:00"
        }
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nCreating test items...")
    for item_data in items:
        try:
            response = requests.post(
                f"{BACKEND_URL}/items/",
                json=item_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"✅ Created {item_data['type']} item: {item_data['title']}")
            else:
                print(f"❌ Failed to create {item_data['title']}: {response.text}")
        except Exception as e:
            print(f"❌ Error creating {item_data['title']}: {str(e)}")

def login_user(username, password):
    """Login and get access token"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            data={
                "username": username,
                "password": password
            }
        )
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Logged in as {username}")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def main():
    print("=" * 60)
    print("POPULATING PRODUCTION DATABASE WITH TEST DATA")
    print("=" * 60)
    
    # Step 1: Create users
    print("\n📝 Step 1: Creating test users...")
    create_test_users()
    
    # Step 2: Login as one user
    print("\n🔐 Step 2: Logging in...")
    token = login_user("priyesh", "priyesh123")
    
    if token:
        # Step 3: Create items
        print("\n📦 Step 3: Creating test items...")
        create_test_items(token)
    
    print("\n" + "=" * 60)
    print("✅ DONE! Your production database now has test data!")
    print("=" * 60)
    print("\n🔑 Test Credentials:")
    print("   Admin: admin@test.com / admin123")
    print("   User: priyesh@test.com / priyesh123")
    print("   User: user1@test.com / user123")
    print("\n🌐 Test your app at: https://lost-found-pri.vercel.app")

if __name__ == "__main__":
    main()
