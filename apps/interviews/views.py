from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def mock_interview_page(request):
    """Mock interview practice page"""
    return render(request, 'mock_interview.html')
