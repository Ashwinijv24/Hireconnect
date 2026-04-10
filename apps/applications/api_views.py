from rest_framework import generics, status, views, parsers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.db.models import Q
from .models import Application, SavedJob, CandidateProfile, JobMatch
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer, 
    ApplicationUpdateSerializer, SavedJobSerializer, CandidateProfileSerializer,
    ApplicationMessageSerializer, JobMatchSerializer
)
from .models import ApplicationMessage
from apps.jobs.models import Job


class ApplicationCreateAPIView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user already applied
        job_id = serializer.validated_data['job'].id
        user = request.user
        if Application.objects.filter(job_id=job_id, candidate__user=user).exists():
            return Response(
                {'error': 'You have already applied to this job'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate resume is provided
        if 'resume' not in request.data or not request.data['resume']:
            return Response(
                {'error': 'Resume is required to apply for this job'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(
            {'message': 'Application submitted successfully', 'application': serializer.data},
            status=status.HTTP_201_CREATED
        )


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(
            candidate__user=self.request.user
        ).select_related('job', 'job__company').prefetch_related('messages')


class JobApplicationsAPIView(generics.ListAPIView):
    """Employer view: see all applications for their jobs"""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return Application.objects.filter(
            job_id=job_id,
            job__posted_by=self.request.user
        ).select_related('candidate', 'candidate__user', 'job', 'job__company').prefetch_related('messages')

    def list(self, request, *args, **kwargs):
        """
        When employer opens the applications list, mark them as viewed (tracking feature).
        """
        qs = self.get_queryset().filter(viewed_by_employer=False)
        now = timezone.now()
        if qs.exists():
            qs.update(viewed_by_employer=True, viewed_at=now)
        return super().list(request, *args, **kwargs)


class ApplicationUpdateAPIView(generics.UpdateAPIView):
    """Employer can update application status"""
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(job__posted_by=self.request.user)


class SaveJobAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'error': 'job_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        saved_job, created = SavedJob.objects.get_or_create(
            user=request.user,
            job_id=job_id
        )
        
        if created:
            return Response({'message': 'Job saved successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Job already saved'}, status=status.HTTP_200_OK)


class UnsaveJobAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, job_id):
        try:
            saved_job = SavedJob.objects.get(user=request.user, job_id=job_id)
            saved_job.delete()
            return Response({'message': 'Job unsaved successfully'}, status=status.HTTP_200_OK)
        except SavedJob.DoesNotExist:
            return Response({'error': 'Job not found in saved list'}, status=status.HTTP_404_NOT_FOUND)


class MySavedJobsAPIView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related('job', 'job__company')


class CandidateProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_object(self):
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ApplicationMessagesAPIView(views.APIView):
    """
    Candidate + Employer messages for a specific application (HR response feature).

    - Candidate can read/write messages for their own applications
    - Employer can read/write messages for applications to their jobs
    """

    permission_classes = [IsAuthenticated]

    def _get_application_for_user(self, request, application_id: int) -> Application:
        try:
            app = Application.objects.select_related('job', 'job__posted_by', 'candidate', 'candidate__user').get(id=application_id)
        except Application.DoesNotExist:
            raise ValidationError({'error': 'Application not found'})

        if request.user.is_superuser:
            return app

        is_candidate_owner = (app.candidate.user_id == request.user.id)
        is_employer_owner = (app.job.posted_by_id == request.user.id)

        if not (is_candidate_owner or is_employer_owner):
            raise PermissionDenied('Not allowed')
        return app

    def get(self, request, pk: int):
        app = self._get_application_for_user(request, pk)

        qs = ApplicationMessage.objects.filter(application=app).select_related('sender')
        if app.candidate.user_id == request.user.id:
            qs = qs.filter(is_internal=False)  # candidates never see internal notes

        data = ApplicationMessageSerializer(qs, many=True).data
        return Response({'application_id': app.id, 'messages': data})

    def post(self, request, pk: int):
        app = self._get_application_for_user(request, pk)

        message = (request.data.get('message') or '').strip()
        new_status = (request.data.get('new_status') or '').strip()
        is_internal = bool(request.data.get('is_internal', False))

        if not message:
            raise ValidationError({'message': 'Message is required'})

        is_candidate_owner = (app.candidate.user_id == request.user.id)
        is_employer_owner = (app.job.posted_by_id == request.user.id)

        if is_candidate_owner:
            sender_role = 'candidate'
            is_internal = False  # force public for candidate
            new_status = ''      # candidate cannot change status
        elif is_employer_owner:
            sender_role = 'employer'
            # employer may optionally update status (Naukri-style shortlist/reject/etc.)
            if new_status and new_status not in dict(Application.STATUS_CHOICES):
                raise ValidationError({'new_status': 'Invalid status'})
        else:
            sender_role = 'admin'
            is_internal = False

        msg = ApplicationMessage.objects.create(
            application=app,
            sender=request.user,
            sender_role=sender_role,
            message=message,
            new_status=new_status,
            is_internal=is_internal,
        )

        # Apply status update and response time tracking (first employer response)
        if sender_role == 'employer':
            if new_status and app.status != new_status:
                app.status = new_status
                app.save(update_fields=['status', 'updated_at'])

            if app.response_time_hours is None:
                delta = timezone.now() - app.applied_at
                app.response_time_hours = max(0, int(delta.total_seconds() // 3600))
                app.save(update_fields=['response_time_hours', 'updated_at'])

        return Response(ApplicationMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class JobMatchAPIView(views.APIView):
    """Calculate and return match score for a specific job"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate match
        match = JobMatch.calculate_match(job, request.user)
        serializer = JobMatchSerializer(match)
        
        return Response(serializer.data)


class RecommendedJobsAPIView(generics.ListAPIView):
    """Get recommended jobs based on user profile (match score >= 70%)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get all active jobs
        jobs = Job.objects.filter(is_active=True)[:50]  # Limit to 50 for performance
        
        # Calculate matches for all jobs
        matches = []
        for job in jobs:
            match = JobMatch.calculate_match(job, request.user)
            if match.is_recommended:  # >= 70%
                matches.append(match)
        
        # Sort by score
        matches.sort(key=lambda x: x.overall_score, reverse=True)
        
        serializer = JobMatchSerializer(matches[:20], many=True)  # Top 20
        return Response({
            'count': len(matches),
            'recommended_jobs': serializer.data
        })


class BulkCalculateMatchesAPIView(views.APIView):
    """Calculate matches for multiple jobs at once"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        job_ids = request.data.get('job_ids', [])
        
        if not job_ids:
            return Response({'error': 'job_ids required'}, status=status.HTTP_400_BAD_REQUEST)
        
        jobs = Job.objects.filter(id__in=job_ids, is_active=True)
        matches = []
        
        for job in jobs:
            match = JobMatch.calculate_match(job, request.user)
            matches.append({
                'job_id': job.id,
                'job_title': job.title,
                'company': job.company.name,
                'overall_score': match.overall_score,
                'is_recommended': match.is_recommended
            })
        
        return Response({'matches': matches})
