#!/usr/bin/env python3
"""
Simple test script to verify the Restaurant API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_user_registration():
    """Test user registration endpoint"""
    print("Testing user registration...")
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✓ User registration successful")
        return response.json()
    else:
        print(f"✗ User registration failed: {response.text}")
        return None

def test_user_login(email, password):
    """Test user login endpoint"""
    print("Testing user login...")
    url = f"{BASE_URL}/auth/login/"
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ User login successful")
        return response.json()
    else:
        print(f"✗ User login failed: {response.text}")
        return None

def test_menu_list():
    """Test menu list endpoint (public)"""
    print("Testing menu list...")
    url = f"{BASE_URL}/menu/"
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Menu list accessible")
        return response.json()
    else:
        print(f"✗ Menu list failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint with JWT token"""
    print("Testing protected endpoint (user profile)...")
    url = f"{BASE_URL}/auth/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Protected endpoint accessible with token")
        return response.json()
    else:
        print(f"✗ Protected endpoint failed: {response.text}")
        return None

def main():
    print("=== Restaurant API Test ===\n")
    
    # Test 1: User Registration
    registration_result = test_user_registration()
    if not registration_result:
        print("Registration failed, stopping tests.")
        return
    
    print(f"User created: {registration_result['user']['username']}")
    access_token = registration_result['tokens']['access']
    print(f"Access token received: {access_token[:20]}...\n")
    
    # Test 2: User Login
    login_result = test_user_login("test@example.com", "testpassword123")
    if login_result:
        print(f"Login successful for: {login_result['user']['email']}\n")
    
    # Test 3: Menu List (public endpoint)
    menu_result = test_menu_list()
    if menu_result:
        print(f"Menu items found: {len(menu_result)}\n")
    
    # Test 4: Protected endpoint
    profile_result = test_protected_endpoint(access_token)
    if profile_result:
        print(f"Profile data: {profile_result}\n")
    
    print("=== API Tests Completed ===")

if __name__ == "__main__":
    main()
