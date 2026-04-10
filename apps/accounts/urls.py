from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, admin_views, api_views

router = DefaultRouter()
router.register(r'profile', api_views.UserProfileViewSet, basename='profile')
router.register(r'education', api_views.EducationViewSet, basename='education')
router.register(r'experience', api_views.ExperienceViewSet, basename='experience')
router.register(r'certifications', api_views.CertificationViewSet, basename='certifications')

app_name = 'accounts'

urlpatterns = [
    # Template views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/admin/dashboard/', admin_views.AdminDashboardAPIView.as_view(), name='api_admin_dashboard'),
]
