"""
Register Fresh User with Corrected Configuration
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

print("\n" + "="*80)
print("REGISTERING FRESH USER WITH CORRECT CONFIG")
print("="*80 + "\n")

timestamp = datetime.now().strftime("%H%M%S")
test_data = {
    "email": "priyesh.code@gmail.com",
    "username": f"priyeshfresh{timestamp}",
    "full_name": "Priyesh Fresh Test",
    "password": "TestPassword123!"
}

print(f"Registering: {test_data['username']} with email: {test_data['email']}")

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=test_data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Registration successful!")
        print("✅ NEW verification email sent to: priyesh.code@gmail.com")
        print("\n🔗 This email will have the CORRECT link:")
        print("   http://localhost:3000/verify-email/[token]")
        print("\n📧 Check your email for the NEW verification link!")
    else:
        print(f"\n❌ Failed: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "="*80)
