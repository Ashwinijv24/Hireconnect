from .models import Notification


def create_notification(user, notification_type, title, message, application=None, job=None):
    """
    Helper function to create notifications
    
    Args:
        user: User instance
        notification_type: Type of notification (from NOTIFICATION_TYPES)
        title: Notification title
        message: Notification message
        application: Optional Application instance
        job: Optional Job instance
    """
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        application=application,
        job=job,
    )
