#!/usr/bin/env python
"""
Diagnostic script to check backend setup
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.jobs.models import Job
from apps.applications.models import Application

User = get_user_model()

print("=" * 60)
print("HireConnect Backend Diagnostic")
print("=" * 60)

# Check 1: Database
print("\n1. Database Check:")
try:
    user_count = User.objects.count()
    print(f"   ✓ Database connected")
    print(f"   ✓ Users in database: {user_count}")
except Exception as e:
    print(f"   ✗ Database error: {e}")
    sys.exit(1)

# Check 2: Settings
print("\n2. Settings Check:")
print(f"   ✓ DEBUG: {settings.DEBUG}")
print(f"   ✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"   ✓ CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")

# Check 3: REST Framework
print("\n3. REST Framework Check:")
print(f"   ✓ Authentication: {settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])}")
print(f"   ✓ Permissions: {settings.REST_FRAMEWORK.get('DEFAULT_PERMISSION_CLASSES', [])}")

# Check 4: Models
print("\n4. Models Check:")
try:
    job_count = Job.objects.count()
    app_count = Application.objects.count()
    print(f"   ✓ Jobs in database: {job_count}")
    print(f"   ✓ Applications in database: {app_count}")
except Exception as e:
    print(f"   ✗ Model error: {e}")

# Check 5: Test User
print("\n5. Test User Check:")
try:
    test_user = User.objects.filter(username='poo').first()
    if test_user:
        print(f"   ✓ Test user 'poo' exists")
        print(f"   ✓ Email: {test_user.email}")
        print(f"   ✓ Is candidate: {test_user.is_candidate}")
    else:
        print(f"   ✗ Test user 'poo' not found")
        print(f"   → Create user with: python manage.py createsuperuser")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check 6: Imports
print("\n6. Import Check:")
try:
    from rest_framework.authtoken.models import Token
    print(f"   ✓ Token model imported")
except Exception as e:
    print(f"   ✗ Token import error: {e}")

try:
    from apps.accounts.api_views import register, login, logout, health_check
    print(f"   ✓ API views imported")
except Exception as e:
    print(f"   ✗ API views import error: {e}")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
