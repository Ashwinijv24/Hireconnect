from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MockInterviewViewSet, VideoInterviewViewSet, InterviewQuestionViewSet
from .views import mock_interview_page

router = DefaultRouter()
router.register(r'mock-interviews', MockInterviewViewSet, basename='mock-interview')
router.register(r'video-interviews', VideoInterviewViewSet, basename='video-interview')
router.register(r'questions', InterviewQuestionViewSet, basename='interview-question')

urlpatterns = [
    path('', include(router.urls)),
    path('practice/', mock_interview_page, name='mock-interview-page'),
]
