import requests
import json

API_URL = "http://localhost:8000/api/v1"

def register_user(email, password, name):
    try:
        response = requests.post(f"{API_URL}/auth/register", json={
            "email": email,
            "password": password,
            "username": email.split("@")[0],
            "full_name": name
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        # If already exists, try login
        login_data = {"username": email, "password": password}
        response = requests.post(f"{API_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            return response.json()["access_token"]
        print(f"Failed to register/login {email}: {response.text}")
        return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def create_found_item(token):
    headers = {"Authorization": f"Bearer {token}"}
    item_data = {
        "title": "Found Wallet Test",
        "description": "Found a black leather wallet",
        "type": "found",
        "status": "active",
        "location": "Central Park",
        "category_id": 1, # Assuming 1 exists
        "date_found": "2023-10-27T10:00:00"
    }
    # First get categories to be safe
    try:
        cats = requests.get(f"{API_URL}/items/categories")
        if cats.status_code == 200 and len(cats.json()) > 0:
            item_data["category_id"] = cats.json()[0]["id"]
        
        response = requests.post(f"{API_URL}/items/", json=item_data, headers=headers)
        if response.status_code == 200:
            return response.json()["id"]
        print(f"Failed to create item: {response.text}")
        return None
    except Exception as e:
        print(f"Error creating item: {e}")
        return None

def claim_item(token, item_id):
    headers = {"Authorization": f"Bearer {token}"}
    claim_data = {
        "proof_description": "It has my ID inside.",
        "proof_image_url": None
    }
    try:
        response = requests.post(f"{API_URL}/items/{item_id}/claim", json=claim_data, headers=headers)
        print(f"Claim Response Status: {response.status_code}")
        print(f"Claim Response Body: {response.text}")
    except Exception as e:
        print(f"Error claiming item: {e}")

def main():
    print("--- Starting Debug Claim ---")
    
    # User A (Finder)
    token_a = register_user("finder_debug_2@example.com", "Test1234!", "Finder User")
    if not token_a: return

    # User A reports item
    item_id = create_found_item(token_a)
    if not item_id: return
    print(f"Created Found Item ID: {item_id}")

    # User B (Claimant)
    token_b = register_user("claimant_debug_2@example.com", "Test1234!", "Claimant User")
    if not token_b: return

    # User B claims item
    print(f"User B attempting to claim Item {item_id}...")
    claim_item(token_b, item_id)

if __name__ == "__main__":
    main()
