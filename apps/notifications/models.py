from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('application_status', 'Application Status Changed'),
        ('application_received', 'Application Received'),
        ('job_match', 'Job Match Found'),
        ('saved_job_update', 'Saved Job Updated'),
        ('message', 'New Message'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('job_posted', 'New Job Posted'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional foreign key references
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
