"""
Test Email Verification Flow
Register user with priyesh.code@gmail.com and verify the flow
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*80)
print("TESTING EMAIL VERIFICATION FLOW")
print("="*80 + "\n")

# Step 1: Register new user
print("Step 1: Registering user with priyesh.code@gmail.com...")
timestamp = datetime.now().strftime("%H%M%S")
test_data = {
    "email": "priyesh.code@gmail.com",
    "username": f"priyeshtest{timestamp}",
    "full_name": "Priyesh Test User",
    "password": "TestPassword123!"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Registration successful!")
        print("✅ Verification email should be sent to: priyesh.code@gmail.com")
        print("\nNext steps:")
        print("1. Check your email inbox (priyesh.code@gmail.com)")
        print("2. Click the verification link in the email")
        print("3. You should see 'Email Verified!' message")
        print("4. You'll be redirected to login page")
        print("\n⚠️  IMPORTANT: The link should look like:")
        print("   http://localhost:3000/verify-email/[some-token]")
    else:
        print(f"\n❌ Registration failed: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "="*80)
print("Waiting for you to click the verification link...")
print("="*80 + "\n")

# Step 2: Test login BEFORE verification (should fail)
print("\nStep 2: Testing login BEFORE email verification (should fail with 403)...")
login_data = {
    "username": test_data["email"],
    "password": test_data["password"]
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 403:
        print("\n✅ CORRECT! Login blocked - email not verified")
        print("✅ User must verify email first")
    else:
        print("\n⚠️  Unexpected response - should be 403")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "="*80)
print("TEST INSTRUCTIONS:")
print("="*80)
print("1. Check email: priyesh.code@gmail.com")
print("2. Click verification link")
print("3. Verify you see 'Email Verified!' page")
print("4. After verification, run: python test_login_after_verify.py")
print("="*80 + "\n")
