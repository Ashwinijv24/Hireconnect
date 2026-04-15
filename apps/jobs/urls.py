from django.urls import path
from . import api_views, employer_views
app_name = 'jobs'
urlpatterns = [
    # Public API endpoints
    path('api/jobs/', api_views.JobListAPIView.as_view(), name='api_job_list'),
    path('api/jobs/<int:pk>/', api_views.JobDetailAPIView.as_view(), name='api_job_detail'),
    path('api/jobs/latest/', api_views.LatestJobsAPIView.as_view(), name='api_latest_jobs'),
    path('api/categories/', api_views.JobCategoriesAPIView.as_view(), name='api_categories'),
    
    # Employer API endpoints
    path('api/employer/jobs/', employer_views.MyJobsAPIView.as_view(), name='api_my_jobs'),
    path('api/employer/jobs/create/', employer_views.JobCreateAPIView.as_view(), name='api_job_create'),
    path('api/employer/jobs/<int:pk>/update/', employer_views.JobUpdateAPIView.as_view(), name='api_job_update'),
    path('api/employer/jobs/<int:pk>/delete/', employer_views.JobDeleteAPIView.as_view(), name='api_job_delete'),
]
