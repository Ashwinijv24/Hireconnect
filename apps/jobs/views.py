from django.shortcuts import render, get_object_or_404
from .models import Job
def home(request):
    latest = Job.objects.order_by('-posted_at')[:6]
    return render(request, 'home.html', {'latest': latest})
def job_list(request):
    qs = Job.objects.order_by('-posted_at')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
    return render(request, 'jobs/list.html', {'jobs': qs})
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/detail.html', {'job': job})
