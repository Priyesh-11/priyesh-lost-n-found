import requests

# Test CORS preflight
print("Testing CORS Configuration...")
print("=" * 80)

url = "http://localhost:8000/api/v1/auth/register"

# Test OPTIONS request (CORS preflight)
print("1. Testing CORS preflight (OPTIONS request)...")
try:
    response = requests.options(url, headers={
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    })
    print(f"   Status Code: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
except Exception as e:
    print(f"   Error: {str(e)}")

print("\n2. Testing actual registration POST from localhost:3000 origin...")
try:
    data = {
        "email": "corstest@example.com",
        "username": "corstest",
        "password": "Test1234",
        "full_name": "CORS Test User"
    }
    response = requests.post(url, json=data, headers={'Origin': 'http://localhost:3000'})
    print(f"   Status Code: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    if response.status_code == 200:
        print("   ✅ Registration successful!")
    else:
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {str(e)}")

print("\n" + "=" * 80)
