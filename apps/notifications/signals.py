"""
Signal handlers to automatically create notifications for key events
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.applications.models import Application
from .models import Notification
from .utils import create_notification


@receiver(post_save, sender=Application)
def notify_on_application_status_change(sender, instance, created, update_fields, **kwargs):
    """Create notification when application status changes"""
    
    if created:
        # Notify candidate that application was submitted
        create_notification(
            user=instance.candidate.user,
            notification_type='application_received',
            title='Application Submitted',
            message=f'Your application for {instance.job.title} at {instance.job.company.name} has been submitted.',
            application=instance,
            job=instance.job,
        )
        
        # Notify employer of new application
        if instance.job.posted_by:
            create_notification(
                user=instance.job.posted_by,
                notification_type='application_received',
                title='New Application Received',
                message=f'{instance.candidate.user.get_full_name() or instance.candidate.user.username} applied for {instance.job.title}.',
                application=instance,
                job=instance.job,
            )
    else:
        # Check if status field was actually updated
        if update_fields and 'status' in update_fields:
            # Notify candidate of status change
            if instance.status in ['shortlisted', 'interview', 'rejected', 'hired']:
                status_messages = {
                    'shortlisted': 'You have been shortlisted!',
                    'interview': 'An interview has been scheduled for you.',
                    'rejected': 'Unfortunately, your application was not selected.',
                    'hired': 'Congratulations! You have been hired!',
                }
                
                create_notification(
                    user=instance.candidate.user,
                    notification_type='application_status',
                    title=f'Application {instance.get_status_display()}',
                    message=status_messages.get(instance.status, f'Your application status has been updated to {instance.get_status_display()}.'),
                    application=instance,
                    job=instance.job,
                )
