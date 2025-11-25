import requests
import json

# Test Registration
print("Testing Registration Endpoint...")
print("=" * 80)

url = "http://localhost:8000/api/v1/auth/register"
data = {
    "email": "newtestuser@example.com",
    "username": "newtestuser",
    "password": "Test1234",
    "full_name": "New Test User",
    "phone": "+1234567890"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "=" * 80)
