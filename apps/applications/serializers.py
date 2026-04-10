from rest_framework import serializers
from .models import Application, CandidateProfile, SavedJob, ApplicationMessage, JobMatch
from apps.jobs.serializers import JobListSerializer


class CandidateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CandidateProfile
        fields = ['id', 'username', 'email', 'headline', 'bio', 'phone', 'location', 
                  'skills', 'experience_years', 'linkedin_url', 'portfolio_url', 'resume', 'resume_url']
    
    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
        return None


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    candidate = CandidateProfileSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    resume_url = serializers.SerializerMethodField()
    viewed_by_employer = serializers.BooleanField(read_only=True)
    viewed_at = serializers.DateTimeField(read_only=True)
    response_time_hours = serializers.IntegerField(read_only=True)
    latest_public_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'candidate', 'cover_letter', 'resume', 'resume_url', 'status', 'status_display',
                  'applied_at', 'updated_at', 'notes',
                  'viewed_by_employer', 'viewed_at', 'response_time_hours', 'latest_public_message']
        read_only_fields = ['applied_at', 'updated_at']
    
    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
        return None

    def get_latest_public_message(self, obj):
        # latest non-internal message (usually HR response); safe for candidates
        msg = obj.messages.filter(is_internal=False).order_by('-created_at').first()
        if not msg:
            return None
        return {
            'id': msg.id,
            'sender_role': msg.sender_role,
            'message': msg.message,
            'new_status': msg.new_status or None,
            'created_at': msg.created_at,
        }


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'cover_letter', 'resume']
    
    def create(self, validated_data):
        user = self.context['request'].user
        profile, _ = CandidateProfile.objects.get_or_create(user=user)
        validated_data['candidate'] = profile
        return super().create(validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'notes']


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'saved_at']
        read_only_fields = ['saved_at']


class ApplicationMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = ApplicationMessage
        fields = ['id', 'application', 'sender', 'sender_username', 'sender_role', 'message',
                  'new_status', 'is_internal', 'created_at']
        read_only_fields = ['id', 'sender', 'sender_username', 'sender_role', 'created_at']


class JobMatchSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)
    candidate_name = serializers.CharField(source='candidate.username', read_only=True)
    match_level = serializers.SerializerMethodField()
    
    class Meta:
        model = JobMatch
        fields = ['id', 'job', 'candidate_name', 'overall_score', 'skills_score', 
                  'experience_score', 'education_score', 'location_score',
                  'matched_skills', 'missing_skills', 'matched_keywords',
                  'is_recommended', 'match_level', 'calculated_at']
    
    def get_match_level(self, obj):
        score = obj.overall_score
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Very Good'
        elif score >= 70:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        else:
            return 'Low'
