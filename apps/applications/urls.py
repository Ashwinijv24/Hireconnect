from django.urls import path
from . import api_views, user_views

app_name = 'applications'

urlpatterns = [
    # User views (template-based)
    path('my-applications/', user_views.my_applications, name='my-applications'),
    path('applications/<int:application_id>/', user_views.application_detail, name='application-detail'),
    
    # Candidate endpoints
    path('api/applications/', api_views.MyApplicationsAPIView.as_view(), name='api_my_applications'),
    path('api/applications/apply/', api_views.ApplicationCreateAPIView.as_view(), name='api_apply'),
    path('api/profile/', api_views.CandidateProfileAPIView.as_view(), name='api_profile'),
    path('api/saved-jobs/', api_views.MySavedJobsAPIView.as_view(), name='api_saved_jobs'),
    path('api/save-job/', api_views.SaveJobAPIView.as_view(), name='api_save_job'),
    path('api/unsave-job/<int:job_id>/', api_views.UnsaveJobAPIView.as_view(), name='api_unsave_job'),
    
    # Employer endpoints
    path('api/jobs/<int:job_id>/applications/', api_views.JobApplicationsAPIView.as_view(), name='api_job_applications'),
    path('api/applications/<int:pk>/update/', api_views.ApplicationUpdateAPIView.as_view(), name='api_application_update'),

    # HR response / messages
    path('api/applications/<int:pk>/messages/', api_views.ApplicationMessagesAPIView.as_view(), name='api_application_messages'),
    
    # AI Resume Matching
    path('api/jobs/<int:job_id>/match/', api_views.JobMatchAPIView.as_view(), name='api_job_match'),
    path('api/recommended-jobs/', api_views.RecommendedJobsAPIView.as_view(), name='api_recommended_jobs'),
    path('api/calculate-matches/', api_views.BulkCalculateMatchesAPIView.as_view(), name='api_calculate_matches'),
]
