"""
Test Login After Email Verification
This script tests if login works AFTER email is verified
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*80)
print("TESTING LOGIN AFTER EMAIL VERIFICATION")
print("="*80 + "\n")

# Get username from user
username = input("Enter the username you registered with: ")
password = "TestPassword123!"

login_data = {
    "username": "priyesh.code@gmail.com",  # Use email for login
    "password": password
}

print(f"\nAttempting login with: {login_data['username']}")

try:
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ LOGIN SUCCESSFUL!")
        print(f"✅ Access Token: {data['access_token'][:50]}...")
        print(f"✅ Refresh Token: {data['refresh_token'][:50]}...")
        print("\n🎉 EMAIL VERIFICATION FLOW WORKING PERFECTLY!")
    elif response.status_code == 403:
        print("\n❌ Login blocked - Email not verified yet")
        print("⚠️  Please click the verification link in your email first")
    else:
        print(f"\n❌ Login failed: {response.json()}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "="*80)
