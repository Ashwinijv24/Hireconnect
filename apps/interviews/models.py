from django.db import models
from django.conf import settings
from apps.applications.models import Application
from apps.jobs.models import Job


class MockInterview(models.Model):
    """Mock interview practice sessions for candidates"""
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mock_interviews')
    job_category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    questions = models.JSONField(default=list)  # List of questions asked
    answers = models.JSONField(default=list)  # Candidate's answers
    ai_feedback = models.TextField(blank=True)  # AI-generated feedback
    score = models.IntegerField(null=True, blank=True)  # Overall score out of 100
    duration_minutes = models.IntegerField(default=30)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Mock Interview - {self.candidate.username} - {self.job_category}"


class VideoInterview(models.Model):
    """Video interview recordings and scheduling"""
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='video_interviews')
    scheduled_at = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    meeting_link = models.URLField(blank=True)  # Zoom/Meet link
    recording_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    interviewer_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at']
    
    def __str__(self):
        return f"Video Interview - {self.application.candidate.user.username} - {self.application.job.title}"


class InterviewQuestion(models.Model):
    """Question bank for mock interviews"""
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('situational', 'Situational'),
        ('general', 'General'),
    )
    
    QUESTION_TYPE_CHOICES = (
        ('mcq', 'Multiple Choice'),
        ('text', 'Text Answer'),
    )
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='mcq')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    job_role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=MockInterview.DIFFICULTY_CHOICES)
    
    # MCQ specific fields
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=1, blank=True, help_text='A, B, C, or D')
    explanation = models.TextField(blank=True, help_text='Explanation of the correct answer')
    
    # Text question fields
    sample_answer = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job_role} - {self.question_text[:50]}"
