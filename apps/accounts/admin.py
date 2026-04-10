from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Education, Experience, Certification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'is_employer', 'is_candidate', 'is_staff']
    list_filter = ['is_employer', 'is_candidate', 'is_staff', 'is_superuser']


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'designation', 'company', 'experience_years']
    search_fields = ['user__username', 'full_name', 'designation', 'company']
    inlines = [EducationInline, ExperienceInline, CertificationInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['profile', 'degree', 'field_of_study', 'institution', 'start_date', 'end_date']
    list_filter = ['is_current']
    search_fields = ['degree', 'field_of_study', 'institution']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['profile', 'job_title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    search_fields = ['job_title', 'company']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['profile', 'name', 'issuing_organization', 'issue_date', 'expiry_date']
    search_fields = ['name', 'issuing_organization']


# Register our custom User admin
admin.site.register(User, UserAdmin)
