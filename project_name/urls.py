from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.jobs.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.applications.urls')),
    path('api/ai/', include('apps.ai_assistant.urls')),
    path('api/interviews/', include('apps.interviews.urls')),
    path('notifications/', include('apps.notifications.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
