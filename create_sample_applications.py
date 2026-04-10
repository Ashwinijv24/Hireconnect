#!/usr/bin/env python
"""
Script to create sample applications for testing the My Applications page.
Run this from the backend directory: python create_sample_applications.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')
django.setup()

from apps.accounts.models import User, UserProfile
from apps.jobs.models import Job, JobCategory, Company
from apps.applications.models import Application, CandidateProfile
from datetime import datetime, timedelta

def create_sample_applications():
    """Create sample applications for testing"""
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testcandidate',
        defaults={
            'email': 'testcandidate@example.com',
            'first_name': 'Test',
            'last_name': 'Candidate'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✓ Created test user: {user.username}")
    else:
        print(f"✓ Using existing user: {user.username}")
    
    # Get or create user profile
    user_profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': 'Test Candidate',
            'profile_summary': 'Experienced software developer'
        }
    )
    
    # Get or create candidate profile
    candidate_profile, _ = CandidateProfile.objects.get_or_create(
        user=user,
        defaults={
            'bio': 'Experienced software developer',
            'skills': 'Python, Django, JavaScript, React'
        }
    )
    print(f"✓ Candidate profile ready")
    
    # Get existing companies or create if needed
    companies = list(Company.objects.all())
    if not companies:
        company_names = ['Tech Corp', 'Innovation Labs', 'Digital Solutions', 'Cloud Systems']
        for name in company_names:
            company = Company.objects.create(
                name=name,
                description=f'{name} is a leading technology company'
            )
            companies.append(company)
    print(f"✓ Using {len(companies)} companies")
    
    # Get or create job category
    category, _ = JobCategory.objects.get_or_create(
        name='Technology',
        defaults={'description': 'Technology and IT jobs'}
    )
    
    # Create sample jobs and applications
    job_titles = [
        ('Senior Software Engineer', 120000, 160000, 'pending'),
        ('Full Stack Developer', 90000, 130000, 'reviewing'),
        ('Frontend Developer', 80000, 120000, 'shortlisted'),
        ('DevOps Engineer', 100000, 150000, 'interview'),
        ('Data Scientist', 110000, 160000, 'rejected'),
        ('Backend Developer', 85000, 125000, 'hired'),
    ]
    
    applications_created = 0
    now = datetime.now()
    
    for idx, (title, min_sal, max_sal, status) in enumerate(job_titles):
        # Create job
        job, _ = Job.objects.get_or_create(
            title=title,
            company=companies[idx % len(companies)],
            defaults={
                'description': f'We are looking for a {title} to join our team.',
                'location': ['San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX'][idx % 4],
                'employment_type': ['full_time', 'contract', 'part_time'][idx % 3],
                'salary_min': min_sal,
                'salary_max': max_sal,
                'is_remote': idx % 2 == 0,
                'is_featured': idx < 2,
                'category': category,
                'posted_at': now - timedelta(days=idx*5)
            }
        )
        
        # Create application
        app, created = Application.objects.get_or_create(
            job=job,
            candidate=candidate_profile,
            defaults={
                'status': status,
                'applied_at': now - timedelta(days=idx*5),
                'updated_at': now - timedelta(days=max(0, idx*5-2)),
                'cover_letter': f'I am very interested in the {title} position at {job.company.name}. With my experience in software development, I believe I would be a great fit for this role.',
                'response_time_hours': [24, 48, 72, 96, None, 12][idx] if status != 'pending' else None
            }
        )
        
        if created:
            applications_created += 1
            print(f"✓ Created application: {title} at {job.company.name} - Status: {status}")
        else:
            print(f"✓ Application already exists: {title} at {job.company.name}")
    
    print(f"\n✅ Successfully created {applications_created} sample applications!")
    print(f"\nTest Credentials:")
    print(f"  Username: testcandidate")
    print(f"  Password: testpass123")
    print(f"\nVisit: http://127.0.0.1:8000/my-applications/")

if __name__ == '__main__':
    create_sample_applications()
