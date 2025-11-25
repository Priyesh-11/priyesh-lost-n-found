"""
Test script to verify SMTP email sending is working
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*80)
print("Testing SMTP Email Functionality")
print("="*80 + "\n")

# Test 1: Register a new user (should trigger verification email)
print("Test 1: Registering new user to test verification email...")
test_data = {
    "email": "test_smtp_2025@example.com",
    "username": "testsmtp2025",
    "full_name": "SMTP Test User",
    "password": "TestSMTP123!"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=test_data)
    if response.status_code == 200:
        print("✅ User registered successfully!")
        print("✅ Check your email (priyeshsingh1101@gmail.com) for verification email")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(f"Details: {response.text}")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "="*80)
print("Test complete! Check the backend console for email sending logs.")
print("="*80)
