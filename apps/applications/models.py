from django.db import models
from apps.jobs.models import Job
from django.conf import settings
from django.utils import timezone
import re
from difflib import SequenceMatcher


class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    experience_years = models.IntegerField(null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Portfolio fields
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    portfolio_projects = models.JSONField(default=list, blank=True)  # List of projects
    certifications = models.JSONField(default=list, blank=True)  # List of certifications
    
    def __str__(self):
        return self.user.username


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'job']
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text='Internal notes from employer')
    
    # Application tracking fields
    viewed_by_employer = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    response_time_hours = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.candidate.user.username} -> {self.job.title}"


class ApplicationMessage(models.Model):
    """
    Simple in-app message thread between candidate and employer for a specific application.
    Used to represent "HR response" and candidate follow-ups.
    """

    SENDER_ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='application_messages')
    sender_role = models.CharField(max_length=20, choices=SENDER_ROLE_CHOICES)
    message = models.TextField()

    # Optional metadata
    new_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES, blank=True)
    is_internal = models.BooleanField(default=False, help_text='Internal employer note (not visible to candidate)')

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_role} -> App {self.application_id}"


class JobMatch(models.Model):
    """AI-powered job matching scores for candidates"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='matches')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_matches')
    
    # Match scores (0-100)
    overall_score = models.IntegerField(default=0, help_text='Overall match percentage')
    skills_score = models.IntegerField(default=0, help_text='Skills match score')
    experience_score = models.IntegerField(default=0, help_text='Experience match score')
    education_score = models.IntegerField(default=0, help_text='Education match score')
    location_score = models.IntegerField(default=0, help_text='Location match score')
    
    # Matching details
    matched_skills = models.JSONField(default=list, help_text='Skills that match')
    missing_skills = models.JSONField(default=list, help_text='Skills candidate is missing')
    matched_keywords = models.JSONField(default=list, help_text='Keywords that match')
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now=True)
    is_recommended = models.BooleanField(default=False, help_text='Recommended match (>70%)')
    
    class Meta:
        unique_together = ['job', 'candidate']
        ordering = ['-overall_score']
    
    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title} ({self.overall_score}%)"
    
    @staticmethod
    def calculate_match(job, user):
        """Calculate match score between a job and a candidate"""
        from apps.accounts.models import UserProfile, Education, Experience
        
        # Get user profile and related data
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None
        
        education_list = Education.objects.filter(profile__user=user) if profile else []
        experience_list = Experience.objects.filter(profile__user=user) if profile else []
        
        # Initialize scores
        skills_score = 0
        experience_score = 0
        education_score = 0
        location_score = 0
        matched_skills = []
        missing_skills = []
        matched_keywords = []
        
        # 1. Skills Matching (40% weight)
        if profile and profile.skills:
            candidate_skills = [s.strip().lower() for s in profile.skills.split(',')]
            job_text = f"{job.title} {job.description} {job.requirements}".lower()
            
            # Extract skills from job description
            job_skills = []
            common_skills = [
                'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
                'django', 'flask', 'spring', 'sql', 'mongodb', 'aws', 'azure', 'docker',
                'kubernetes', 'git', 'agile', 'scrum', 'html', 'css', 'typescript',
                'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust',
                'machine learning', 'ai', 'data science', 'devops', 'ci/cd'
            ]
            
            for skill in common_skills:
                if skill in job_text:
                    job_skills.append(skill)
            
            # Calculate skill matches
            for skill in candidate_skills:
                if any(skill in js or js in skill for js in job_skills):
                    matched_skills.append(skill)
                    skills_score += 1
            
            # Find missing skills
            for skill in job_skills:
                if not any(skill in cs or cs in skill for cs in candidate_skills):
                    missing_skills.append(skill)
            
            # Calculate percentage
            if job_skills:
                skills_score = int((len(matched_skills) / len(job_skills)) * 100)
            else:
                skills_score = 50  # Default if no specific skills found
        
        # 2. Experience Matching (30% weight)
        if profile and profile.experience_years is not None:
            candidate_exp = profile.experience_years
            
            # Extract experience requirements from job description
            exp_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', job.requirements.lower() if job.requirements else job.description.lower())
            required_exp = int(exp_match.group(1)) if exp_match else 0
            
            if required_exp == 0:
                experience_score = 80  # No specific requirement
            elif candidate_exp >= required_exp:
                experience_score = 100
            elif candidate_exp >= required_exp * 0.7:
                experience_score = 80
            elif candidate_exp >= required_exp * 0.5:
                experience_score = 60
            else:
                experience_score = 40
        else:
            experience_score = 50  # Default
        
        # 3. Education Matching (20% weight)
        if education_list:
            job_text_lower = f"{job.title} {job.description} {job.requirements}".lower()
            
            # Check for degree requirements
            has_bachelors = any('bachelor' in e.degree.lower() for e in education_list)
            has_masters = any('master' in e.degree.lower() for e in education_list)
            has_phd = any('phd' in e.degree.lower() or 'doctor' in e.degree.lower() for e in education_list)
            
            requires_degree = 'bachelor' in job_text_lower or 'degree' in job_text_lower
            requires_masters = 'master' in job_text_lower
            requires_phd = 'phd' in job_text_lower or 'doctorate' in job_text_lower
            
            if requires_phd and has_phd:
                education_score = 100
            elif requires_masters and has_masters:
                education_score = 100
            elif requires_degree and has_bachelors:
                education_score = 100
            elif has_masters or has_phd:
                education_score = 90
            elif has_bachelors:
                education_score = 80
            else:
                education_score = 60
        else:
            education_score = 50  # Default
        
        # 4. Location Matching (10% weight)
        if profile and profile.location and job.location:
            candidate_location = profile.location.lower()
            job_location = job.location.lower()
            
            if job.is_remote:
                location_score = 100
            elif candidate_location in job_location or job_location in candidate_location:
                location_score = 100
            else:
                # Check for same city/state
                similarity = SequenceMatcher(None, candidate_location, job_location).ratio()
                location_score = int(similarity * 100)
        else:
            location_score = job.is_remote and 100 or 50
        
        # 5. Keyword Matching
        if profile:
            profile_text = f"{profile.profile_summary} {profile.designation}".lower()
            job_keywords = re.findall(r'\b\w+\b', job.title.lower())
            
            for keyword in job_keywords:
                if len(keyword) > 3 and keyword in profile_text:
                    matched_keywords.append(keyword)
        
        # Calculate overall score with weights
        overall_score = int(
            (skills_score * 0.40) +
            (experience_score * 0.30) +
            (education_score * 0.20) +
            (location_score * 0.10)
        )
        
        # Create or update match
        match, created = JobMatch.objects.update_or_create(
            job=job,
            candidate=user,
            defaults={
                'overall_score': overall_score,
                'skills_score': skills_score,
                'experience_score': experience_score,
                'education_score': education_score,
                'location_score': location_score,
                'matched_skills': matched_skills[:10],  # Limit to top 10
                'missing_skills': missing_skills[:10],
                'matched_keywords': matched_keywords[:10],
                'is_recommended': overall_score >= 70
            }
        )
        
        return match
