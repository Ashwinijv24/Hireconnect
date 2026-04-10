from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employer = form.cleaned_data.get('is_employer')
            user.is_candidate = not user.is_employer
            user.save()
            login(request, user)
            return redirect('jobs:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
from django.contrib.auth.forms import AuthenticationForm
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'jobs:home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        # Add placeholders to form fields
        form.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        })
        form.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    return render(request, 'accounts/login.html', {'form': form})
from django.contrib.auth.decorators import login_required
@login_required
def logout_view(request):
    logout(request)
    return redirect('jobs:home')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('jobs:home')
    return render(request, 'admin_dashboard.html')


@login_required
def debug_dashboard_view(request):
    return render(request, 'debug_dashboard.html')


@login_required
def profile_view(request):
    """User profile page"""
    return render(request, 'accounts/profile.html')
