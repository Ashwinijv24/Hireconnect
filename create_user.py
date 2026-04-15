#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create test user if doesn't exist
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
    print(f"✓ User created: {user.username}")
else:
    # Update password
    user.set_password('password')
    user.save()
    print(f"✓ User updated: {user.username}")

print(f"✓ Email: {user.email}")
print(f"✓ Is candidate: {user.is_candidate}")
print(f"✓ Ready to login!")
