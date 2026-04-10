from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required


def chat_view(request):
    """Render AI chatbot page"""
    return render(request, 'assistant_chat.html')


def salary_insights_view(request):
    """Render salary insights page"""
    return render(request, 'assistant_salary.html')


def cover_letter_view(request):
    """Render cover letter generator page"""
    return render(request, 'assistant_cover_letter.html')
