from rest_framework import serializers
from .models import MockInterview, VideoInterview, InterviewQuestion


class MockInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockInterview
        fields = ['id', 'job_category', 'difficulty', 'questions', 'answers', 
                  'ai_feedback', 'score', 'duration_minutes', 'completed', 
                  'created_at', 'completed_at']


class VideoInterviewSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='application.candidate.user.get_full_name', read_only=True)
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    
    class Meta:
        model = VideoInterview
        fields = ['id', 'application', 'candidate_name', 'job_title', 'scheduled_at', 
                  'duration_minutes', 'meeting_link', 'recording_url', 'status', 
                  'notes', 'interviewer_name', 'created_at', 'updated_at']


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['id', 'question_text', 'question_type', 'category', 'job_role', 'difficulty',
                  'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 
                  'explanation', 'sample_answer', 'created_at']
