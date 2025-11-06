from django.contrib import admin
from .models import JobPosting, Application
from core.admin_actions import export_as_csv

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'is_draft', 'is_closed', 'created_at')
    list_filter = ('is_draft', 'is_closed', 'remote')
    search_fields = ('title', 'description', 'recruiter__company_name')
    actions = [export_as_csv]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'applicant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('listing__title', 'applicant__first_name', 'applicant__last_name')
    actions = [export_as_csv]
