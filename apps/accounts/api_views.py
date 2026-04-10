from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserProfile, Education, Experience, Certification
from .serializers import (
    UserProfileSerializer, EducationSerializer, 
    ExperienceSerializer, CertificationSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for user profile management"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EducationViewSet(viewsets.ModelViewSet):
    """API endpoint for education management"""
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return Education.objects.filter(profile=profile)
    
    def perform_create(self, serializer):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class ExperienceViewSet(viewsets.ModelViewSet):
    """API endpoint for experience management"""
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return Experience.objects.filter(profile=profile)
    
    def perform_create(self, serializer):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class CertificationViewSet(viewsets.ModelViewSet):
    """API endpoint for certification management"""
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return Certification.objects.filter(profile=profile)
    
    def perform_create(self, serializer):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)
