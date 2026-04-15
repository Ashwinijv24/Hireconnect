from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):  # noqa: F841
    """Root API endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'HireConnect API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/accounts/api/health/',
            'auth': {
                'login': '/accounts/api/login/',
                'register': '/accounts/api/register/',
                'logout': '/accounts/api/logout/',
                'current_user': '/accounts/api/current-user/',
            },
            'jobs': {
                'list': '/api/jobs/',
                'detail': '/api/jobs/{id}/',
                'latest': '/api/jobs/latest/',
                'categories': '/api/categories/',
            },
            'profile': {
                'me': '/accounts/api/profile/me/',
                'update': '/accounts/api/profile/update_profile/',
            },
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
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
