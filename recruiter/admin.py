from django.contrib import admin
from accounts.models import Recruiter
from core.admin_actions import export_as_csv

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'company_name')
    search_fields = ('first_name', 'last_name', 'company_name', 'user__username')
    actions = [export_as_csv]
