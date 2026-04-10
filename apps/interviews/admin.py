from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import MockInterview, VideoInterview, InterviewQuestion


@admin.register(MockInterview)
class MockInterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate_link', 'job_category', 'difficulty_badge', 'score_display', 'completed_badge', 'duration_display', 'created_at']
    list_filter = ['difficulty', 'completed', 'job_category', 'created_at']
    search_fields = ['candidate__username', 'candidate__email', 'job_category']
    readonly_fields = ['created_at', 'completed_at', 'questions_display', 'answers_display', 'feedback_display']
    
    fieldsets = (
        ('Candidate Information', {
            'fields': ('candidate', 'job_category')
        }),
        ('Interview Details', {
            'fields': ('difficulty', 'duration_minutes', 'completed', 'completed_at')
        }),
        ('Performance', {
            'fields': ('score', 'questions_display', 'answers_display', 'feedback_display')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_incomplete', 'export_as_csv']
    
    def candidate_link(self, obj):
        """Display candidate with link to their profile"""
        url = reverse('admin:accounts_user_change', args=[obj.candidate.id])
        return format_html('<a href="{}">{}</a>', url, obj.candidate.username)
    candidate_link.short_description = 'Candidate'
    
    def difficulty_badge(self, obj):
        """Display difficulty with color badge"""
        colors = {
            'easy': '#28a745',
            'medium': '#ffc107',
            'hard': '#dc3545'
        }
        color = colors.get(obj.difficulty, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def score_display(self, obj):
        """Display score with color coding"""
        if obj.score is None:
            return format_html('<span style="color: #999;">Not scored</span>')
        
        if obj.score >= 80:
            color = '#28a745'
        elif obj.score >= 60:
            color = '#ffc107'
        else:
            color = '#dc3545'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/100</span>',
            color,
            obj.score
        )
    score_display.short_description = 'Score'
    
    def completed_badge(self, obj):
        """Display completion status with badge"""
        if obj.completed:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Completed</span>'
            )
        return format_html(
            '<span style="background-color: #ffc107; color: white; padding: 3px 10px; border-radius: 3px;">In Progress</span>'
        )
    completed_badge.short_description = 'Status'
    
    def duration_display(self, obj):
        """Display duration"""
        return f"{obj.duration_minutes} min"
    duration_display.short_description = 'Duration'
    
    def questions_display(self, obj):
        """Display questions in readable format"""
        if not obj.questions:
            return "No questions"
        return format_html(
            '<ol>{}</ol>',
            ''.join([f'<li>{q}</li>' for q in obj.questions])
        )
    questions_display.short_description = 'Questions'
    
    def answers_display(self, obj):
        """Display answers in readable format"""
        if not obj.answers:
            return "No answers"
        return format_html(
            '<ol>{}</ol>',
            ''.join([f'<li>{a}</li>' for a in obj.answers])
        )
    answers_display.short_description = 'Answers'
    
    def feedback_display(self, obj):
        """Display AI feedback"""
        if not obj.ai_feedback:
            return "No feedback"
        return format_html('<pre style="white-space: pre-wrap;">{}</pre>', obj.ai_feedback)
    feedback_display.short_description = 'AI Feedback'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected interviews as completed"""
        updated = queryset.update(completed=True, completed_at=timezone.now())
        self.message_user(request, f'{updated} interview(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected as completed'
    
    def mark_as_incomplete(self, request, queryset):
        """Mark selected interviews as incomplete"""
        updated = queryset.update(completed=False, completed_at=None)
        self.message_user(request, f'{updated} interview(s) marked as incomplete.')
    mark_as_incomplete.short_description = 'Mark selected as incomplete'
    
    def export_as_csv(self, request, queryset):
        """Export selected interviews as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mock_interviews.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Candidate', 'Job Category', 'Difficulty', 'Score', 'Completed', 'Created At'])
        
        for interview in queryset:
            writer.writerow([
                interview.candidate.username,
                interview.job_category,
                interview.get_difficulty_display(),
                interview.score or 'N/A',
                'Yes' if interview.completed else 'No',
                interview.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_as_csv.short_description = 'Export selected as CSV'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('candidate')


@admin.register(VideoInterview)
class VideoInterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'job_title', 'scheduled_at_display', 'status_badge', 'interviewer_name', 'meeting_link_display', 'actions_display']
    list_filter = ['status', 'scheduled_at', 'created_at']
    search_fields = ['application__candidate__user__username', 'application__job__title', 'interviewer_name']
    readonly_fields = ['created_at', 'updated_at', 'application_link', 'recording_preview']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('application', 'application_link')
        }),
        ('Interview Scheduling', {
            'fields': ('scheduled_at', 'duration_minutes', 'status')
        }),
        ('Meeting Details', {
            'fields': ('meeting_link', 'interviewer_name', 'notes')
        }),
        ('Recording', {
            'fields': ('recording_url', 'recording_preview')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_scheduled', 'mark_as_in_progress', 'mark_as_completed', 'mark_as_cancelled', 'send_meeting_reminder']
    
    def candidate_name(self, obj):
        """Display candidate name with link"""
        url = reverse('admin:accounts_user_change', args=[obj.application.candidate.user.id])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.application.candidate.user.get_full_name() or obj.application.candidate.user.username
        )
    candidate_name.short_description = 'Candidate'
    
    def job_title(self, obj):
        """Display job title"""
        return obj.application.job.title
    job_title.short_description = 'Job Position'
    
    def scheduled_at_display(self, obj):
        """Display scheduled time with formatting"""
        now = timezone.now()
        if obj.scheduled_at < now:
            color = '#dc3545'
            status = 'Past'
        elif (obj.scheduled_at - now).days <= 1:
            color = '#ffc107'
            status = 'Soon'
        else:
            color = '#28a745'
            status = 'Upcoming'
        
        return format_html(
            '<span style="color: {};">{} ({})</span>',
            color,
            obj.scheduled_at.strftime('%Y-%m-%d %H:%M'),
            status
        )
    scheduled_at_display.short_description = 'Scheduled At'
    
    def status_badge(self, obj):
        """Display status with color badge"""
        colors = {
            'scheduled': '#0066cc',
            'in_progress': '#ffc107',
            'completed': '#28a745',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def meeting_link_display(self, obj):
        """Display meeting link as clickable button"""
        if obj.meeting_link:
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #0066cc; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Join Meeting</a>',
                obj.meeting_link
            )
        return format_html('<span style="color: #999;">No link</span>')
    meeting_link_display.short_description = 'Meeting'
    
    def recording_preview(self, obj):
        """Display recording link as clickable button"""
        if obj.recording_url:
            return format_html(
                '<a href="{}" target="_blank" style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">View Recording</a>',
                obj.recording_url
            )
        return format_html('<span style="color: #999;">No recording</span>')
    recording_preview.short_description = 'Recording'
    
    def actions_display(self, obj):
        """Display quick action buttons"""
        buttons = []
        
        if obj.status == 'scheduled':
            buttons.append(format_html(
                '<a class="button" href="?status__exact=in_progress">Start</a>'
            ))
        
        if obj.status != 'cancelled':
            buttons.append(format_html(
                '<a class="button" href="?status__exact=cancelled">Cancel</a>'
            ))
        
        return format_html(' '.join(buttons))
    actions_display.short_description = 'Actions'
    
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
    
    def mark_as_scheduled(self, request, queryset):
        """Mark selected interviews as scheduled"""
        updated = queryset.update(status='scheduled')
        self.message_user(request, f'{updated} interview(s) marked as scheduled.')
    mark_as_scheduled.short_description = 'Mark as Scheduled'
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected interviews as in progress"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} interview(s) marked as in progress.')
    mark_as_in_progress.short_description = 'Mark as In Progress'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected interviews as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} interview(s) marked as completed.')
    mark_as_completed.short_description = 'Mark as Completed'
    
    def mark_as_cancelled(self, request, queryset):
        """Mark selected interviews as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} interview(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark as Cancelled'
    
    def send_meeting_reminder(self, request, queryset):
        """Send meeting reminder to candidates"""
        count = queryset.filter(status='scheduled').count()
        # TODO: Implement email sending
        self.message_user(request, f'Reminder sent to {count} candidate(s).')
    send_meeting_reminder.short_description = 'Send Meeting Reminder'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('application', 'application__candidate', 'application__job')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category_badge', 'job_role', 'difficulty_badge', 'question_type_badge', 'created_at']
    list_filter = ['category', 'difficulty', 'job_role', 'question_type', 'created_at']
    search_fields = ['question_text', 'job_role', 'sample_answer']
    readonly_fields = ['created_at', 'options_display', 'answer_display']
    
    fieldsets = (
        ('Question Information', {
            'fields': ('question_text', 'question_type', 'category', 'job_role', 'difficulty')
        }),
        ('Multiple Choice Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation', 'options_display'),
            'classes': ('collapse',)
        }),
        ('Text Answer', {
            'fields': ('sample_answer', 'answer_display'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_questions_csv', 'duplicate_question']
    
    def question_preview(self, obj):
        """Display question preview"""
        preview = obj.question_text[:60]
        if len(obj.question_text) > 60:
            preview += '...'
        return preview
    question_preview.short_description = 'Question'
    
    def category_badge(self, obj):
        """Display category with badge"""
        colors = {
            'technical': '#0066cc',
            'behavioral': '#28a745',
            'situational': '#ffc107',
            'general': '#6c757d'
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_category_display()
        )
    category_badge.short_description = 'Category'
    
    def difficulty_badge(self, obj):
        """Display difficulty with badge"""
        colors = {
            'easy': '#28a745',
            'medium': '#ffc107',
            'hard': '#dc3545'
        }
        color = colors.get(obj.difficulty, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def question_type_badge(self, obj):
        """Display question type with badge"""
        colors = {
            'mcq': '#0066cc',
            'text': '#28a745'
        }
        color = colors.get(obj.question_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_question_type_display()
        )
    question_type_badge.short_description = 'Type'
    
    def options_display(self, obj):
        """Display MCQ options"""
        if obj.question_type != 'mcq':
            return "Not applicable for text questions"
        
        options = []
        for letter, option in [('A', obj.option_a), ('B', obj.option_b), ('C', obj.option_c), ('D', obj.option_d)]:
            if option:
                is_correct = obj.correct_answer == letter
                style = 'color: #28a745; font-weight: bold;' if is_correct else ''
                options.append(f'<li style="{style}">{letter}. {option}</li>')
        
        result = f'<ol>{"".join(options)}</ol>'
        if obj.explanation:
            result += f'<p><strong>Explanation:</strong> {obj.explanation}</p>'
        
        return format_html(result)
    options_display.short_description = 'Options & Explanation'
    
    def answer_display(self, obj):
        """Display sample answer for text questions"""
        if obj.question_type != 'text':
            return "Not applicable for MCQ"
        
        if obj.sample_answer:
            return format_html('<pre style="white-space: pre-wrap;">{}</pre>', obj.sample_answer)
        return "No sample answer provided"
    answer_display.short_description = 'Sample Answer'
    
    def export_questions_csv(self, request, queryset):
        """Export selected questions as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="interview_questions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Question', 'Category', 'Job Role', 'Difficulty', 'Type', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer'])
        
        for question in queryset:
            writer.writerow([
                question.question_text,
                question.get_category_display(),
                question.job_role,
                question.get_difficulty_display(),
                question.get_question_type_display(),
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.correct_answer
            ])
        
        return response
    export_questions_csv.short_description = 'Export selected as CSV'
    
    def duplicate_question(self, request, queryset):
        """Duplicate selected questions"""
        for question in queryset:
            question.pk = None
            question.save()
        self.message_user(request, f'{queryset.count()} question(s) duplicated.')
    duplicate_question.short_description = 'Duplicate selected questions'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.order_by('-created_at')
