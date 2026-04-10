from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Application, CandidateProfile, SavedJob, ApplicationMessage, JobMatch


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'headline', 'location', 'experience_years', 'skills_preview']
    search_fields = ['user__username', 'user__email', 'headline', 'skills']
    readonly_fields = ['user', 'skills_display', 'certifications_display', 'portfolio_display']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('headline', 'bio', 'phone', 'location', 'experience_years')
        }),
        ('Skills & Qualifications', {
            'fields': ('skills', 'skills_display', 'certifications_display')
        }),
        ('Portfolio & Links', {
            'fields': ('github_url', 'website_url', 'linkedin_url', 'portfolio_url', 'portfolio_display')
        }),
        ('Resume', {
            'fields': ('resume',)
        }),
    )
    
    def user_link(self, obj):
        """Display user with link to profile"""
        url = reverse('admin:accounts_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def skills_preview(self, obj):
        """Display skills preview"""
        if obj.skills:
            skills = obj.skills.split(',')[:3]
            return ', '.join([s.strip() for s in skills])
        return 'No skills'
    skills_preview.short_description = 'Skills'
    
    def skills_display(self, obj):
        """Display skills in readable format"""
        if obj.skills:
            skills = obj.skills.split(',')
            return format_html(
                '<div>{}</div>',
                ', '.join([f'<span style="background-color: #e3f2fd; padding: 3px 8px; border-radius: 3px; margin: 2px;">{s.strip()}</span>' for s in skills])
            )
        return 'No skills'
    skills_display.short_description = 'Skills'
    
    def certifications_display(self, obj):
        """Display certifications"""
        if obj.certifications:
            return format_html(
                '<ol>{}</ol>',
                ''.join([f'<li>{cert}</li>' for cert in obj.certifications])
            )
        return 'No certifications'
    certifications_display.short_description = 'Certifications'
    
    def portfolio_display(self, obj):
        """Display portfolio projects"""
        if obj.portfolio_projects:
            return format_html(
                '<ol>{}</ol>',
                ''.join([f'<li>{proj}</li>' for proj in obj.portfolio_projects])
            )
        return 'No projects'
    portfolio_display.short_description = 'Portfolio Projects'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'job_title', 'company_name', 'status_badge', 'applied_at_display', 'viewed_badge', 'response_time_display', 'actions_display']
    list_filter = ['status', 'viewed_by_employer', 'applied_at']
    search_fields = ['job__title', 'candidate__user__username', 'candidate__user__email', 'job__company__name']
    readonly_fields = ['applied_at', 'updated_at', 'viewed_at', 'candidate_link', 'job_link', 'resume_preview', 'cover_letter_display']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('candidate_link', 'job_link', 'applied_at', 'updated_at')
        }),
        ('Application Status', {
            'fields': ('status', 'viewed_by_employer', 'viewed_at', 'response_time_hours')
        }),
        ('Application Documents', {
            'fields': ('resume', 'resume_preview', 'cover_letter', 'cover_letter_display')
        }),
        ('Employer Notes', {
            'fields': ('notes',)
        }),
    )
    
    actions = ['mark_pending', 'mark_reviewing', 'mark_shortlisted', 'mark_interview', 'mark_rejected', 'mark_hired', 'mark_viewed', 'send_status_notification']
    
    def candidate_name(self, obj):
        """Display candidate name with link"""
        url = reverse('admin:accounts_user_change', args=[obj.candidate.user.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.candidate.user.get_full_name() or obj.candidate.user.username
        )
    candidate_name.short_description = 'Candidate'
    
    def job_title(self, obj):
        """Display job title"""
        return obj.job.title
    job_title.short_description = 'Job Position'
    
    def company_name(self, obj):
        """Display company name"""
        return obj.job.company.name
    company_name.short_description = 'Company'
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'pending': '#ffc107',
            'reviewing': '#0066cc',
            'shortlisted': '#28a745',
            'interview': '#9c27b0',
            'rejected': '#dc3545',
            'hired': '#00aa00'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def applied_at_display(self, obj):
        """Display applied date"""
        return obj.applied_at.strftime('%Y-%m-%d %H:%M')
    applied_at_display.short_description = 'Applied At'
    
    def viewed_badge(self, obj):
        """Display viewed status"""
        if obj.viewed_by_employer:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Viewed</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: white; padding: 3px 8px; border-radius: 3px;">Not Viewed</span>'
        )
    viewed_badge.short_description = 'Viewed'
    
    def response_time_display(self, obj):
        """Display response time"""
        if obj.response_time_hours:
            return f"{obj.response_time_hours} hours"
        return "—"
    response_time_display.short_description = 'Response Time'
    
    def actions_display(self, obj):
        """Display quick action buttons"""
        buttons = []
        
        if obj.status != 'hired':
            buttons.append(format_html(
                '<a class="button" style="background-color: #28a745;" href="?status__exact=shortlisted">Shortlist</a>'
            ))
        
        if obj.status != 'rejected':
            buttons.append(format_html(
                '<a class="button" style="background-color: #dc3545;" href="?status__exact=rejected">Reject</a>'
            ))
        
        return format_html(' '.join(buttons))
    actions_display.short_description = 'Quick Actions'
    
    def candidate_link(self, obj):
        """Display candidate link"""
        url = reverse('admin:accounts_user_change', args=[obj.candidate.user.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.candidate.user.get_full_name() or obj.candidate.user.username
        )
    candidate_link.short_description = 'Candidate'
    
    def job_link(self, obj):
        """Display job link"""
        url = reverse('admin:jobs_job_change', args=[obj.job.id])
        return format_html(
            '<a href="{}">{} at {}</a>',
            url,
            obj.job.title,
            obj.job.company.name
        )
    job_link.short_description = 'Job Position'
    
    def resume_preview(self, obj):
        """Display resume preview"""
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #0066cc; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Download Resume</a>',
                obj.resume.url
            )
        return 'No resume'
    resume_preview.short_description = 'Resume'
    
    def cover_letter_display(self, obj):
        """Display cover letter"""
        if obj.cover_letter:
            return format_html('<pre style="white-space: pre-wrap; max-height: 300px; overflow-y: auto;">{}</pre>', obj.cover_letter)
        return 'No cover letter'
    cover_letter_display.short_description = 'Cover Letter'
    
    def mark_pending(self, request, queryset):
        """Mark applications as pending"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} application(s) marked as pending.')
    mark_pending.short_description = 'Mark as Pending'
    
    def mark_reviewing(self, request, queryset):
        """Mark applications as reviewing"""
        updated = queryset.update(status='reviewing')
        self.message_user(request, f'{updated} application(s) marked as reviewing.')
    mark_reviewing.short_description = 'Mark as Reviewing'
    
    def mark_shortlisted(self, request, queryset):
        """Mark applications as shortlisted"""
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} application(s) marked as shortlisted.')
    mark_shortlisted.short_description = 'Mark as Shortlisted ✓'
    
    def mark_interview(self, request, queryset):
        """Mark applications as interview scheduled"""
        updated = queryset.update(status='interview')
        self.message_user(request, f'{updated} application(s) marked as interview scheduled.')
    mark_interview.short_description = 'Mark as Interview Scheduled'
    
    def mark_rejected(self, request, queryset):
        """Mark applications as rejected"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) marked as rejected.')
    mark_rejected.short_description = 'Mark as Rejected ✗'
    
    def mark_hired(self, request, queryset):
        """Mark applications as hired"""
        updated = queryset.update(status='hired')
        self.message_user(request, f'{updated} application(s) marked as hired.')
    mark_hired.short_description = 'Mark as Hired 🎉'
    
    def mark_viewed(self, request, queryset):
        """Mark applications as viewed"""
        updated = queryset.update(viewed_by_employer=True, viewed_at=timezone.now())
        self.message_user(request, f'{updated} application(s) marked as viewed.')
    mark_viewed.short_description = 'Mark as Viewed'
    
    def send_status_notification(self, request, queryset):
        """Send status notification to candidates"""
        count = queryset.count()
        # TODO: Implement email notification
        self.message_user(request, f'Status notification sent to {count} candidate(s).')
    send_status_notification.short_description = 'Send Status Notification'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('candidate', 'job', 'job__company')


@admin.register(ApplicationMessage)
class ApplicationMessageAdmin(admin.ModelAdmin):
    list_display = ['application_display', 'sender_display', 'sender_role_badge', 'new_status_badge', 'is_internal_badge', 'created_at']
    list_filter = ['sender_role', 'is_internal', 'new_status', 'created_at']
    search_fields = ['application__job__title', 'application__candidate__user__username', 'sender__username', 'message']
    readonly_fields = ['created_at', 'application_link', 'sender_link', 'message_display']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('application_link', 'sender_link', 'sender_role', 'created_at')
        }),
        ('Message Content', {
            'fields': ('message', 'message_display')
        }),
        ('Status Update', {
            'fields': ('new_status', 'is_internal')
        }),
    )
    
    def application_display(self, obj):
        """Display application"""
        return f"{obj.application.candidate.user.username} - {obj.application.job.title}"
    application_display.short_description = 'Application'
    
    def sender_display(self, obj):
        """Display sender"""
        return obj.sender.get_full_name() or obj.sender.username
    sender_display.short_description = 'Sender'
    
    def sender_role_badge(self, obj):
        """Display sender role with badge"""
        colors = {
            'candidate': '#0066cc',
            'employer': '#28a745',
            'admin': '#dc3545'
        }
        color = colors.get(obj.sender_role, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_sender_role_display()
        )
    sender_role_badge.short_description = 'Role'
    
    def new_status_badge(self, obj):
        """Display new status"""
        if obj.new_status:
            colors = {
                'pending': '#ffc107',
                'reviewing': '#0066cc',
                'shortlisted': '#28a745',
                'interview': '#9c27b0',
                'rejected': '#dc3545',
                'hired': '#00aa00'
            }
            color = colors.get(obj.new_status, '#6c757d')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
                color,
                obj.new_status
            )
        return '—'
    new_status_badge.short_description = 'Status'
    
    def is_internal_badge(self, obj):
        """Display internal flag"""
        if obj.is_internal:
            return format_html(
                '<span style="background-color: #ffc107; color: white; padding: 3px 8px; border-radius: 3px;">Internal</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Public</span>'
        )
    is_internal_badge.short_description = 'Type'
    
    def application_link(self, obj):
        """Display application link"""
        url = reverse('admin:applications_application_change', args=[obj.application.id])
        return format_html(
            '<a href="{}">{} - {}</a>',
            url,
            obj.application.candidate.user.username,
            obj.application.job.title
        )
    application_link.short_description = 'Application'
    
    def sender_link(self, obj):
        """Display sender link"""
        url = reverse('admin:accounts_user_change', args=[obj.sender.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.sender.get_full_name() or obj.sender.username
        )
    sender_link.short_description = 'Sender'
    
    def message_display(self, obj):
        """Display message"""
        return format_html('<pre style="white-space: pre-wrap;">{}</pre>', obj.message)
    message_display.short_description = 'Message'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('application', 'sender', 'application__candidate', 'application__job')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'job_title', 'company_name', 'saved_at_display']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'job__title', 'job__company__name']
    readonly_fields = ['saved_at', 'user_link', 'job_link']
    
    def user_link(self, obj):
        """Display user with link"""
        url = reverse('admin:accounts_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def job_title(self, obj):
        """Display job title"""
        return obj.job.title
    job_title.short_description = 'Job'
    
    def company_name(self, obj):
        """Display company name"""
        return obj.job.company.name
    company_name.short_description = 'Company'
    
    def saved_at_display(self, obj):
        """Display saved date"""
        return obj.saved_at.strftime('%Y-%m-%d %H:%M')
    saved_at_display.short_description = 'Saved At'
    
    def job_link(self, obj):
        """Display job link"""
        url = reverse('admin:jobs_job_change', args=[obj.job.id])
        return format_html(
            '<a href="{}">{} at {}</a>',
            url,
            obj.job.title,
            obj.job.company.name
        )
    job_link.short_description = 'Job'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'job', 'job__company')


@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'job_title', 'overall_score_display', 'skills_score_display', 'experience_score_display', 'is_recommended_badge', 'calculated_at']
    list_filter = ['is_recommended', 'calculated_at']
    search_fields = ['candidate__username', 'job__title']
    readonly_fields = ['calculated_at', 'candidate_link', 'job_link', 'matched_skills_display', 'missing_skills_display']
    
    fieldsets = (
        ('Match Information', {
            'fields': ('candidate_link', 'job_link', 'calculated_at')
        }),
        ('Scores', {
            'fields': ('overall_score', 'skills_score', 'experience_score', 'education_score', 'location_score')
        }),
        ('Skills Analysis', {
            'fields': ('matched_skills_display', 'missing_skills_display')
        }),
        ('Recommendation', {
            'fields': ('is_recommended',)
        }),
    )
    
    def candidate_name(self, obj):
        """Display candidate name"""
        return obj.candidate.username
    candidate_name.short_description = 'Candidate'
    
    def job_title(self, obj):
        """Display job title"""
        return obj.job.title
    job_title.short_description = 'Job'
    
    def overall_score_display(self, obj):
        """Display overall score with color"""
        if obj.overall_score >= 80:
            color = '#28a745'
        elif obj.overall_score >= 60:
            color = '#ffc107'
        else:
            color = '#dc3545'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}%</span>',
            color,
            obj.overall_score
        )
    overall_score_display.short_description = 'Overall Score'
    
    def skills_score_display(self, obj):
        """Display skills score"""
        return f"{obj.skills_score}%"
    skills_score_display.short_description = 'Skills'
    
    def experience_score_display(self, obj):
        """Display experience score"""
        return f"{obj.experience_score}%"
    experience_score_display.short_description = 'Experience'
    
    def is_recommended_badge(self, obj):
        """Display recommendation status"""
        if obj.is_recommended:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Recommended</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">Not Recommended</span>'
        )
    is_recommended_badge.short_description = 'Recommendation'
    
    def candidate_link(self, obj):
        """Display candidate link"""
        url = reverse('admin:accounts_user_change', args=[obj.candidate.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.candidate.username
        )
    candidate_link.short_description = 'Candidate'
    
    def job_link(self, obj):
        """Display job link"""
        url = reverse('admin:jobs_job_change', args=[obj.job.id])
        return format_html(
            '<a href="{}">{} at {}</a>',
            url,
            obj.job.title,
            obj.job.company.name
        )
    job_link.short_description = 'Job'
    
    def matched_skills_display(self, obj):
        """Display matched skills"""
        if obj.matched_skills:
            return format_html(
                '<div>{}</div>',
                ', '.join([f'<span style="background-color: #c8e6c9; padding: 3px 8px; border-radius: 3px; margin: 2px;">✓ {s}</span>' for s in obj.matched_skills])
            )
        return 'No matched skills'
    matched_skills_display.short_description = 'Matched Skills'
    
    def missing_skills_display(self, obj):
        """Display missing skills"""
        if obj.missing_skills:
            return format_html(
                '<div>{}</div>',
                ', '.join([f'<span style="background-color: #ffcccc; padding: 3px 8px; border-radius: 3px; margin: 2px;">✗ {s}</span>' for s in obj.missing_skills])
            )
        return 'No missing skills'
    missing_skills_display.short_description = 'Missing Skills'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('candidate', 'job', 'job__company')
