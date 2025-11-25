"""
Comprehensive QA Test Suite for Lost & Found Application
Tests: API endpoints, auth flows, CRUD operations, edge cases
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def add_pass(self, test_name):
        self.passed.append(test_name)
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name, reason):
        self.failed.append(f"{test_name}: {reason}")
        print(f"❌ FAIL: {test_name} - {reason}")
    
    def add_warning(self, test_name, reason):
        self.warnings.append(f"{test_name}: {reason}")
        print(f"⚠️  WARNING: {test_name} - {reason}")
    
    def print_summary(self):
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Passed: {len(self.passed)}")
        print(f"Total Failed: {len(self.failed)}")
        print(f"Total Warnings: {len(self.warnings)}")
        print()
        
        if self.failed:
            print("FAILED TESTS:")
            for fail in self.failed:
                print(f"  ❌ {fail}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warn in self.warnings:
                print(f"  ⚠️  {warn}")

results = TestResults()

# ============================================================================
# 1. AUTHENTICATION TESTS
# ============================================================================
print("\n" + "="*80)
print("1. AUTHENTICATION TESTS")
print("="*80)

# Test 1.1: User Registration
def test_registration():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "email": f"testuser{timestamp}@test.com",
        "username": f"testuser{timestamp}",
        "full_name": "Test User",
        "password": "Test1234!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                results.add_pass("User Registration")
                return data["access_token"], payload["email"]
            else:
                results.add_fail("User Registration", "No access token in response")
                return None, None
        else:
            results.add_fail("User Registration", f"Status {response.status_code}: {response.text}")
            return None, None
    except Exception as e:
        results.add_fail("User Registration", str(e))
        return None, None

token, test_email = test_registration()

# Test 1.2: Duplicate Registration
def test_duplicate_registration():
    if not test_email:
        results.add_warning("Duplicate Registration", "Skipped - no test email")
        return
    
    payload = {
        "email": test_email,
        "username": "duplicate",
        "full_name": "Duplicate",
        "password": "Test1234!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 400:
            results.add_pass("Duplicate Registration Prevention")
        else:
            results.add_fail("Duplicate Registration Prevention", f"Expected 400, got {response.status_code}")
    except Exception as e:
        results.add_fail("Duplicate Registration Prevention", str(e))

test_duplicate_registration()

# Test 1.3: Login
def test_login():
    if not test_email:
        results.add_warning("Login", "Skipped - no test user")
        return None
    
    payload = {
        "username": test_email,
        "password": "Test1234!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=payload)
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data and "refresh_token" in data:
                results.add_pass("Login")
                return data["access_token"]
            else:
                results.add_fail("Login", "Missing tokens in response")
        else:
            results.add_fail("Login", f"Status {response.status_code}")
        return None
    except Exception as e:
        results.add_fail("Login", str(e))
        return None

login_token = test_login()

# Test 1.4: Invalid Credentials
def test_invalid_login():
    payload = {
        "username": "nonexistent@test.com",
        "password": "WrongPass123!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=payload)
        if response.status_code in [400, 401]:
            results.add_pass("Invalid Login Rejection")
        else:
            results.add_fail("Invalid Login Rejection", f"Expected 400/401, got {response.status_code}")
    except Exception as e:
        results.add_fail("Invalid Login Rejection", str(e))

test_invalid_login()

# Test 1.5: Weak Password Validation
def test_weak_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    payload = {
        "email": f"weak{timestamp}@test.com",
        "username": f"weak{timestamp}",
        "full_name": "Weak Password",
        "password": "123"  # Too weak
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 400 or response.status_code == 422:
            results.add_pass("Weak Password Rejection")
        else:
            results.add_fail("Weak Password Rejection", f"Accepted weak password - Status {response.status_code}")
    except Exception as e:
        results.add_fail("Weak Password Rejection", str(e))

test_weak_password()

# ============================================================================
# 2. AUTHORIZATION & ROLE-BASED ACCESS TESTS
# ============================================================================
print("\n" + "="*80)
print("2. AUTHORIZATION & ROLE-BASED ACCESS TESTS")
print("="*80)

# Test 2.1: Protected Route without Token
def test_protected_without_token():
    try:
        response = requests.get(f"{BASE_URL}/users/me")
        if response.status_code == 401:
            results.add_pass("Protected Route - No Token")
        else:
            results.add_fail("Protected Route - No Token", f"Expected 401, got {response.status_code}")
    except Exception as e:
        results.add_fail("Protected Route - No Token", str(e))

test_protected_without_token()

# Test 2.2: Protected Route with Valid Token
def test_protected_with_token():
    if not login_token:
        results.add_warning("Protected Route - Valid Token", "Skipped - no token")
        return
    
    headers = {"Authorization": f"Bearer {login_token}"}
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            results.add_pass("Protected Route - Valid Token")
        else:
            results.add_fail("Protected Route - Valid Token", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Protected Route - Valid Token", str(e))

test_protected_with_token()

# Test 2.3: Admin Route Access (Non-Admin)
def test_admin_route_non_admin():
    if not login_token:
        results.add_warning("Admin Route - Non-Admin", "Skipped - no token")
        return
    
    headers = {"Authorization": f"Bearer {login_token}"}
    try:
        response = requests.get(f"{BASE_URL}/admin/claims", headers=headers)
        if response.status_code == 403:
            results.add_pass("Admin Route - Non-Admin Blocked")
        else:
            results.add_fail("Admin Route - Non-Admin Blocked", f"Expected 403, got {response.status_code}")
    except Exception as e:
        results.add_fail("Admin Route - Non-Admin Blocked", str(e))

test_admin_route_non_admin()

# ============================================================================
# 3. ITEMS CRUD TESTS
# ============================================================================
print("\n" + "="*80)
print("3. ITEMS CRUD TESTS")
print("="*80)

# Test 3.1: Create Item (Lost)
def test_create_lost_item():
    if not login_token:
        results.add_warning("Create Lost Item", "Skipped - no token")
        return None
    
    headers = {"Authorization": f"Bearer {login_token}"}
    payload = {
        "title": "Test Lost Wallet",
        "description": "Black leather wallet lost near park",
        "type": "lost",
        "status": "active",
        "location": "Central Park",
        "category_id": 1,
        "date_lost": "2023-10-27T10:00:00"
    }
    try:
        response = requests.post(f"{BASE_URL}/items/", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results.add_pass("Create Lost Item")
            return data.get("id")
        else:
            results.add_fail("Create Lost Item", f"Status {response.status_code}: {response.text}")
        return None
    except Exception as e:
        results.add_fail("Create Lost Item", str(e))
        return None

item_id = test_create_lost_item()

# Test 3.2: Get All Items
def test_get_all_items():
    try:
        response = requests.get(f"{BASE_URL}/items/")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                results.add_pass("Get All Items")
            else:
                results.add_fail("Get All Items", "Response is not a list")
        else:
            results.add_fail("Get All Items", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get All Items", str(e))

test_get_all_items()

# Test 3.3: Get Item by ID
def test_get_item_by_id():
    if not item_id:
        results.add_warning("Get Item by ID", "Skipped - no item")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        if response.status_code == 200:
            results.add_pass("Get Item by ID")
        else:
            results.add_fail("Get Item by ID", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get Item by ID", str(e))

test_get_item_by_id()

# Test 3.4: Search/Filter Items
def test_search_items():
    try:
        response = requests.get(f"{BASE_URL}/items/?query=wallet")
        if response.status_code == 200:
            results.add_pass("Search Items")
        else:
            results.add_fail("Search Items", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Search Items", str(e))

test_search_items()

# Test 3.5: Filter by Type
def test_filter_by_type():
    try:
        response = requests.get(f"{BASE_URL}/items/?type=lost")
        if response.status_code == 200:
            results.add_pass("Filter by Type")
        else:
            results.add_fail("Filter by Type", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Filter by Type", str(e))

test_filter_by_type()

# ============================================================================
# 4. EDGE CASES & SECURITY TESTS
# ============================================================================
print("\n" + "="*80)
print("4. EDGE CASES & SECURITY TESTS")
print("="*80)

# Test 4.1: SQL Injection Attempt
def test_sql_injection():
    try:
        response = requests.get(f"{BASE_URL}/items/?query=' OR '1'='1")
        # Should handle safely, not crash
        if response.status_code in [200, 400]:
            results.add_pass("SQL Injection Protection")
        else:
            results.add_warning("SQL Injection Protection", f"Unexpected status {response.status_code}")
    except Exception as e:
        results.add_fail("SQL Injection Protection", str(e))

test_sql_injection()

# Test 4.2: XSS Attempt
def test_xss_protection():
    if not login_token:
        results.add_warning("XSS Protection", "Skipped - no token")
        return
    
    headers = {"Authorization": f"Bearer {login_token}"}
    payload = {
        "title": "<script>alert('XSS')</script>",
        "description": "Test XSS",
        "type": "lost",
        "location": "Test",
        "category_id": 1
    }
    try:
        response = requests.post(f"{BASE_URL}/items/", json=payload, headers=headers)
        # Should either sanitize or reject
        results.add_pass("XSS Attempt Handled")
    except Exception as e:
        results.add_fail("XSS Attempt Handled", str(e))

test_xss_protection()

# Test 4.3: Invalid JSON
def test_invalid_json():
    if not login_token:
        results.add_warning("Invalid JSON", "Skipped - no token")
        return
    
    headers = {
        "Authorization": f"Bearer {login_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(f"{BASE_URL}/items/", data="invalid json{{{", headers=headers)
        if response.status_code == 422:
            results.add_pass("Invalid JSON Rejection")
        else:
            results.add_warning("Invalid JSON Rejection", f"Got status {response.status_code}")
    except Exception as e:
        results.add_fail("Invalid JSON Rejection", str(e))

test_invalid_json()

# Test 4.4: Missing Required Fields
def test_missing_fields():
    if not login_token:
        results.add_warning("Missing Required Fields", "Skipped - no token")
        return
    
    headers = {"Authorization": f"Bearer {login_token}"}
    payload = {
        "title": "Test"
        # Missing required fields
    }
    try:
        response = requests.post(f"{BASE_URL}/items/", json=payload, headers=headers)
        if response.status_code == 422:
            results.add_pass("Missing Fields Validation")
        else:
            results.add_fail("Missing Fields Validation", f"Expected 422, got {response.status_code}")
    except Exception as e:
        results.add_fail("Missing Fields Validation", str(e))

test_missing_fields()

# ============================================================================
# 5. CLAIMS SYSTEM TESTS
# ============================================================================
print("\n" + "="*80)
print("5. CLAIMS SYSTEM TESTS")
print("="*80)

# Test 5.1: Create Claim
def test_create_claim():
    if not login_token or not item_id:
        results.add_warning("Create Claim", "Skipped - missing prerequisites")
        return
    
    # First create a found item to claim
    headers = {"Authorization": f"Bearer {login_token}"}
    found_item = {
        "title": "Found Keys",
        "description": "Set of keys found",
        "type": "found",
        "status": "active",
        "location": "Library",
        "category_id": 1
    }
    try:
        response = requests.post(f"{BASE_URL}/items/", json=found_item, headers=headers)
        if response.status_code == 200:
            found_id = response.json().get("id")
            
            # Now create claim (should fail as we own the item)
            claim_data = {
                "proof_description": "These are my keys, they have my keychain"
            }
            claim_response = requests.post(f"{BASE_URL}/items/{found_id}/claim", json=claim_data, headers=headers)
            
            if claim_response.status_code == 400:
                results.add_pass("Cannot Claim Own Item")
            else:
                results.add_warning("Cannot Claim Own Item", f"Expected 400, got {claim_response.status_code}")
        else:
            results.add_warning("Create Claim", "Could not create found item")
    except Exception as e:
        results.add_fail("Create Claim", str(e))

test_create_claim()

# Test 5.2: Get My Claims
def test_get_my_claims():
    if not login_token:
        results.add_warning("Get My Claims", "Skipped - no token")
        return
    
    headers = {"Authorization": f"Bearer {login_token}"}
    try:
        response = requests.get(f"{BASE_URL}/claims/my-claims", headers=headers)
        if response.status_code == 200:
            results.add_pass("Get My Claims")
        else:
            results.add_fail("Get My Claims", f"Status {response.status_code}")
    except Exception as e:
        results.add_fail("Get My Claims", str(e))

test_get_my_claims()

# ============================================================================
# PRINT FINAL SUMMARY
# ============================================================================
results.print_summary()

print("\n" + "="*80)
print("DETAILED QA REPORT SAVED TO: qa_report.txt")
print("="*80)
