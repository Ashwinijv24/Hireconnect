from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'chat', api_views.ChatConversationViewSet, basename='chat')
router.register(r'cover-letters', api_views.CoverLetterViewSet, basename='cover-letters')
router.register(r'salary-insights', api_views.SalaryInsightViewSet, basename='salary-insights')

urlpatterns = [
    # Template views
    path('assistant/chat/', views.chat_view, name='assistant-chat'),
    path('assistant/salary/', views.salary_insights_view, name='assistant-salary'),
    path('assistant/cover-letter/', views.cover_letter_view, name='assistant-cover-letter'),
    
    # API endpoints
    path('', include(router.urls)),
]
