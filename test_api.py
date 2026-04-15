#!/usr/bin/env python
"""
Test API endpoints directly
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("HireConnect API Test")
print("=" * 60)

# Create test client
client = Client()

# Test 1: Health check
print("\n1. Testing Health Check:")
try:
    response = client.get('/accounts/api/health/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Create test user if doesn't exist
print("\n2. Creating Test User:")
try:
    user, created = User.objects.get_or_create(
        username='poo',
        defaults={
            'email': 'poo@example.com',
            'is_candidate': True,
            'is_employer': False,
        }
    )
    if created:
        user.set_password('password')
        user.save()
        print(f"   ✓ User created: {user.username}")
    else:
        print(f"   ✓ User already exists: {user.username}")
        # Update password just in case
        user.set_password('password')
        user.save()
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Login
print("\n3. Testing Login:")
try:
    response = client.post(
        '/accounts/api/login/',
        data=json.dumps({'username': 'poo', 'password': 'password'}),
        content_type='application/json'
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Login successful")
        print(f"   Token: {data.get('token', 'N/A')[:20]}...")
        print(f"   User: {data.get('user', {}).get('username')}")
    else:
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Register
print("\n4. Testing Register:")
try:
    response = client.post(
        '/accounts/api/register/',
        data=json.dumps({
            'username': 'testuser123',
            'email': 'test@example.com',
            'password': 'password123',
            'is_employer': False
        }),
        content_type='application/json'
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"   ✓ Registration successful")
        print(f"   User: {data.get('user', {}).get('username')}")
    else:
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
