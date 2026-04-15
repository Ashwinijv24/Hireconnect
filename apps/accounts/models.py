from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Extended user profile with detailed information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Basic Info
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Professional Info
    designation = models.CharField(max_length=200, blank=True, help_text="Current job title")
    company = models.CharField(max_length=200, blank=True, help_text="Current company")
    experience_years = models.IntegerField(default=0, help_text="Total years of experience")
    
    # Profile Summary
    profile_summary = models.TextField(blank=True, help_text="Professional summary/bio")
    
    # Skills
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    
    # Social Links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True, help_text="URL to resume file")
    
    # Preferences
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type_preference = models.CharField(max_length=50, blank=True, choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ])
    remote_preference = models.CharField(max_length=50, blank=True, choices=[
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


class Education(models.Model):
    """User education details"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='education')
    
    degree = models.CharField(max_length=200, help_text="e.g., Bachelor of Science")
    field_of_study = models.CharField(max_length=200, help_text="e.g., Computer Science")
    institution = models.CharField(max_length=200, help_text="University/College name")
    location = models.CharField(max_length=200, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    grade = models.CharField(max_length=50, blank=True, help_text="GPA or percentage")
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study}"


class Experience(models.Model):
    """User work experience"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experience')
    
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    description = models.TextField(blank=True, help_text="Job responsibilities and achievements")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Certification(models.Model):
    """User certifications and licenses"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certifications')
    
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return self.name
