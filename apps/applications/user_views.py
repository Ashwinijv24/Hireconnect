from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Application, CandidateProfile


@login_required
def my_applications(request):
    """Display user's job applications with status tracking"""
    try:
        candidate_profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        candidate_profile = None
    
    # Get all applications for this candidate
    applications = Application.objects.filter(
        candidate__user=request.user
    ).select_related('job', 'job__company').order_by('-applied_at')
    
    # Get filter from request
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    # Calculate statistics
    total_applications = Application.objects.filter(candidate__user=request.user).count()
    pending_count = Application.objects.filter(candidate__user=request.user, status='pending').count()
    reviewing_count = Application.objects.filter(candidate__user=request.user, status='reviewing').count()
    shortlisted_count = Application.objects.filter(candidate__user=request.user, status='shortlisted').count()
    interview_count = Application.objects.filter(candidate__user=request.user, status='interview').count()
    rejected_count = Application.objects.filter(candidate__user=request.user, status='rejected').count()
    hired_count = Application.objects.filter(candidate__user=request.user, status='hired').count()
    
    context = {
        'applications': applications,
        'candidate_profile': candidate_profile,
        'status_filter': status_filter,
        'total_applications': total_applications,
        'pending_count': pending_count,
        'reviewing_count': reviewing_count,
        'shortlisted_count': shortlisted_count,
        'interview_count': interview_count,
        'rejected_count': rejected_count,
        'hired_count': hired_count,
    }
    
    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail(request, application_id):
    """Display detailed view of a single application"""
    try:
        application = Application.objects.select_related(
            'job', 'job__company'
        ).prefetch_related('messages').get(
            id=application_id,
            candidate__user=request.user
        )
    except Application.DoesNotExist:
        return render(request, '404.html', status=404)
    
    # Get messages for this application
    messages = application.messages.all().order_by('created_at')
    
    context = {
        'application': application,
        'messages': messages,
    }
    
    return render(request, 'applications/application_detail.html', context)
