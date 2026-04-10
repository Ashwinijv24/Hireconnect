from rest_framework import serializers
from .models import ChatConversation, ChatMessage, CoverLetter, SalaryInsight


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp']


class ChatConversationSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatConversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages']


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ['id', 'job_title', 'company_name', 'content', 'is_ai_generated', 
                  'edited', 'created_at', 'updated_at']


class SalaryInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryInsight
        fields = ['id', 'job_title', 'location', 'experience_level', 'min_salary', 
                  'max_salary', 'median_salary', 'data_points', 'industry', 'last_updated']
