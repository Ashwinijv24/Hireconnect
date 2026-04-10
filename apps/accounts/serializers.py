from rest_framework import serializers
from .models import User, UserProfile, Education, Experience, Certification


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree', 'field_of_study', 'institution', 'location', 
                  'start_date', 'end_date', 'is_current', 'grade', 'description']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'job_title', 'company', 'location', 
                  'start_date', 'end_date', 'is_current', 'description']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'name', 'issuing_organization', 'issue_date', 
                  'expiry_date', 'credential_id', 'credential_url']


class UserProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    skills_list = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'location', 
                  'profile_picture', 'designation', 'company', 'experience_years',
                  'profile_summary', 'skills', 'skills_list', 'linkedin_url', 
                  'github_url', 'portfolio_url', 'expected_salary', 
                  'job_type_preference', 'remote_preference', 'education', 
                  'experience', 'certifications', 'created_at', 'updated_at']
    
    def get_skills_list(self, obj):
        return obj.get_skills_list()
