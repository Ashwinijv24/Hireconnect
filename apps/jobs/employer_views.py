from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobDetailSerializer, JobCreateSerializer


class MyJobsAPIView(generics.ListAPIView):
    """Employer: List all jobs posted by them"""
    serializer_class = JobDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).select_related('company', 'category')


class JobCreateAPIView(generics.CreateAPIView):
    """Employer: Create a new job posting"""
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        from apps.companies.models import Company
        
        # Get or create a company for this employer
        company_name = request.data.get('company_name')
        if company_name:
            company, _ = Company.objects.get_or_create(
                name=company_name,
                defaults={'slug': company_name.lower().replace(' ', '-')}
            )
        else:
            # Use existing company or create default
            company_id = request.data.get('company')
            if company_id:
                company = Company.objects.get(id=company_id)
            else:
                # Create a default company for this employer
                company, _ = Company.objects.get_or_create(
                    name=f"{request.user.username}'s Company",
                    defaults={'slug': f"{request.user.username}-company"}
                )
        
        # Add company to the data
        data = request.data.copy()
        data['company'] = company.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(posted_by=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobUpdateAPIView(generics.UpdateAPIView):
    """Employer: Update their job posting"""
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


class JobDeleteAPIView(generics.DestroyAPIView):
    """Employer: Delete their job posting"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Job deleted successfully'}, status=status.HTTP_200_OK)
