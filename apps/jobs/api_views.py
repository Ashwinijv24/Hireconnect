from rest_framework import generics, filters
from rest_framework.response import Response
from django.db.models import Q
from .models import Job, JobCategory
from .serializers import JobListSerializer, JobDetailSerializer, JobCategorySerializer


class JobListAPIView(generics.ListAPIView):
    serializer_class = JobListSerializer
    
    def get_queryset(self):
        qs = Job.objects.filter(is_active=True).select_related('company', 'category').order_by('-is_featured', '-posted_at')
        
        # Search query
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(location__icontains=location)
        
        # Filter by employment type
        emp_type = self.request.query_params.get('employment_type')
        if emp_type:
            qs = qs.filter(employment_type=emp_type)
        
        # Filter by salary range
        salary_min = self.request.query_params.get('salary_min')
        if salary_min:
            qs = qs.filter(salary_max__gte=salary_min)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        
        # Filter remote jobs
        is_remote = self.request.query_params.get('is_remote')
        if is_remote == 'true':
            qs = qs.filter(is_remote=True)
        
        return qs


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True).select_related('company', 'category')
    serializer_class = JobDetailSerializer
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LatestJobsAPIView(generics.ListAPIView):
    serializer_class = JobListSerializer
    queryset = Job.objects.filter(is_active=True).select_related('company', 'category').order_by('-posted_at')[:6]


class JobCategoriesAPIView(generics.ListAPIView):
    serializer_class = JobCategorySerializer
    queryset = JobCategory.objects.all()
