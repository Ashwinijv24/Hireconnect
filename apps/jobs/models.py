from django.db import models
from apps.companies.models import Company
from django.conf import settings


class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Job Categories'
    
    def __str__(self):
        return self.name


class Job(models.Model):
    EMPLOYMENT_TYPE = (
        ('FT','Full-time'), ('PT','Part-time'), ('CT','Contract'), ('IN','Internship'), ('FL','Freelance')
    )
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posted_jobs')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, help_text='Job requirements')
    responsibilities = models.TextField(blank=True, help_text='Job responsibilities')
    location = models.CharField(max_length=255, blank=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE, default='FT')
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Featured/sponsored listing')
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-posted_at']
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"
