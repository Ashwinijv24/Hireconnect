from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from apps.jobs.models import Job
from apps.applications.models import Application, SavedJob
from apps.companies.models import Company

User = get_user_model()


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # User statistics
        total_users = User.objects.count()
        candidates = User.objects.filter(is_candidate=True).count()
        employers = User.objects.filter(is_employer=True).count()
        admins = User.objects.filter(is_superuser=True).count()
        
        # Job statistics
        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(is_active=True).count()
        featured_jobs = Job.objects.filter(is_featured=True).count()
        remote_jobs = Job.objects.filter(is_remote=True).count()
        
        # Application statistics
        total_applications = Application.objects.count()
        pending_apps = Application.objects.filter(status='pending').count()
        reviewing_apps = Application.objects.filter(status='reviewing').count()
        shortlisted_apps = Application.objects.filter(status='shortlisted').count()
        interview_apps = Application.objects.filter(status='interview').count()
        hired_apps = Application.objects.filter(status='hired').count()
        rejected_apps = Application.objects.filter(status='rejected').count()
        
        # Company statistics
        total_companies = Company.objects.count()
        
        # Saved jobs
        total_saved_jobs = SavedJob.objects.count()
        
        # Top applicants (users with most applications)
        top_applicants = User.objects.filter(
            is_candidate=True
        ).annotate(
            app_count=Count('candidateprofile__application')
        ).filter(app_count__gt=0).order_by('-app_count')[:10].values(
            'id', 'username', 'email', 'first_name', 'last_name', 'app_count'
        )
        
        # Top employers (users with most job posts)
        top_employers = User.objects.filter(
            is_employer=True
        ).annotate(
            job_count=Count('posted_jobs')
        ).filter(job_count__gt=0).order_by('-job_count')[:10].values(
            'id', 'username', 'email', 'first_name', 'last_name', 'job_count'
        )
        
        # Most applied jobs
        most_applied_jobs = Job.objects.annotate(
            app_count=Count('applications')
        ).filter(app_count__gt=0).order_by('-app_count')[:10].values(
            'id', 'title', 'company__name', 'location', 'app_count', 'views_count'
        )
        
        # Most viewed jobs
        most_viewed_jobs = Job.objects.filter(
            views_count__gt=0
        ).order_by('-views_count')[:10].values(
            'id', 'title', 'company__name', 'location', 'views_count'
        )
        
        # Recent applications
        recent_applications = Application.objects.select_related(
            'job', 'job__company', 'candidate', 'candidate__user'
        ).order_by('-applied_at')[:20].values(
            'id',
            'job__title',
            'job__company__name',
            'candidate__user__username',
            'candidate__user__email',
            'status',
            'applied_at'
        )
        
        # All users with details
        all_users = User.objects.annotate(
            applications_count=Count('candidateprofile__application', distinct=True),
            jobs_posted_count=Count('posted_jobs', distinct=True),
            saved_jobs_count=Count('saved_jobs', distinct=True)
        ).values(
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_candidate', 'is_employer', 'is_superuser', 'is_active',
            'date_joined', 'last_login',
            'applications_count', 'jobs_posted_count', 'saved_jobs_count'
        ).order_by('-date_joined')
        
        # All jobs with details
        all_jobs = Job.objects.annotate(
            applications_count=Count('applications')
        ).select_related('company', 'posted_by').values(
            'id', 'title', 'company__name', 'location', 'employment_type',
            'salary_min', 'salary_max', 'is_active', 'is_featured', 'is_remote',
            'posted_at', 'views_count', 'applications_count',
            'posted_by__username', 'posted_by__email'
        ).order_by('-posted_at')
        
        # All applications with details
        all_applications = Application.objects.select_related(
            'job', 'job__company', 'candidate', 'candidate__user'
        ).values(
            'id',
            'job__id',
            'job__title',
            'job__company__name',
            'candidate__user__id',
            'candidate__user__username',
            'candidate__user__email',
            'candidate__user__first_name',
            'candidate__user__last_name',
            'status',
            'applied_at',
            'updated_at',
            'notes'
        ).order_by('-applied_at')
        
        return Response({
            'summary': {
                'users': {
                    'total': total_users,
                    'candidates': candidates,
                    'employers': employers,
                    'admins': admins,
                },
                'jobs': {
                    'total': total_jobs,
                    'active': active_jobs,
                    'featured': featured_jobs,
                    'remote': remote_jobs,
                },
                'applications': {
                    'total': total_applications,
                    'pending': pending_apps,
                    'reviewing': reviewing_apps,
                    'shortlisted': shortlisted_apps,
                    'interview': interview_apps,
                    'hired': hired_apps,
                    'rejected': rejected_apps,
                },
                'companies': total_companies,
                'saved_jobs': total_saved_jobs,
            },
            'top_applicants': list(top_applicants),
            'top_employers': list(top_employers),
            'most_applied_jobs': list(most_applied_jobs),
            'most_viewed_jobs': list(most_viewed_jobs),
            'recent_applications': list(recent_applications),
            'all_users': list(all_users),
            'all_jobs': list(all_jobs),
            'all_applications': list(all_applications),
        })
