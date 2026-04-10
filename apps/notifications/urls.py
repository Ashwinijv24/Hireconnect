from django.urls import path
from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    MarkAsReadAPIView,
    MarkAllAsReadAPIView,
    UnreadCountAPIView,
)
from .views_template import notifications_page

urlpatterns = [
    # Template view
    path('', notifications_page, name='notifications-page'),
    
    # API endpoints
    path('api/', NotificationListAPIView.as_view(), name='notification-list'),
    path('api/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('api/<int:pk>/mark-as-read/', MarkAsReadAPIView.as_view(), name='mark-as-read'),
    path('api/mark-all-as-read/', MarkAllAsReadAPIView.as_view(), name='mark-all-as-read'),
    path('api/unread-count/', UnreadCountAPIView.as_view(), name='unread-count'),
]
