from django.contrib import admin
from .models import ChatConversation, ChatMessage, CoverLetter, SalaryInsight


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'title']
    inlines = [ChatMessageInline]


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'company_name', 'is_ai_generated', 'edited', 'created_at']
    list_filter = ['is_ai_generated', 'edited', 'created_at']
    search_fields = ['user__username', 'job_title', 'company_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SalaryInsight)
class SalaryInsightAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'location', 'experience_level', 'median_salary', 'data_points', 'last_updated']
    list_filter = ['experience_level', 'last_updated']
    search_fields = ['job_title', 'location']
