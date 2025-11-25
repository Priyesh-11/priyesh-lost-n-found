import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": f"db_verify_{int(time.time())}@example.com",  # Unique email
    "username": f"db_verify_{int(time.time())}",           # Unique username
    "password": "TestPassword123!",
    "full_name": "Database Verification User",
    "phone": "+1987654321"
}

def register_user():
    print(f"Attempting to register user: {TEST_USER['email']}")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
        if response.status_code == 200:
            print("✅ Registration successful!")
            print(json.dumps(response.json(), indent=2))
            return True, TEST_USER['email']
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(response.text)
            return False, None
    except Exception as e:
        print(f"❌ Error during registration: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, email = register_user()
    if success:
        # Save the email to a file so the verification script can read it
        with open("last_registered_email.txt", "w") as f:
            f.write(email)
