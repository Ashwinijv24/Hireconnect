from rest_framework import serializers
from .models import Job, JobCategory
from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'website', 'description']


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'slug', 'description']


class JobListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'employment_type', 
                  'employment_type_display', 'salary_min', 'salary_max', 'posted_at',
                  'is_remote', 'is_featured', 'is_active', 'applications_count']
    
    def get_applications_count(self, obj):
        return obj.applications.count()


class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'requirements', 'responsibilities',
                  'company', 'category', 'location', 'employment_type', 'employment_type_display', 
                  'salary_min', 'salary_max', 'is_remote', 'is_featured', 'is_active',
                  'posted_at', 'updated_at', 'views_count', 'applications_count']
    
    def get_applications_count(self, obj):
        return obj.applications.count()


class JobCreateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Job
        fields = ['company', 'category', 'title', 'description', 'requirements', 
                  'responsibilities', 'location', 'employment_type', 'salary_min', 
                  'salary_max', 'is_remote', 'is_featured', 'expires_at']
