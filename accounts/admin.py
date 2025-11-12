from django.contrib import admin
from .models import Applicant
from core.admin_actions import export_as_csv

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'location', 'availability')
    search_fields = ('first_name', 'last_name', 'location', 'skills', 'user__username')
    actions = [export_as_csv]

# Register your models here.
from .models import Applicant, Recruiter, ApplicantPrivacySettings
admin.site.register(ApplicantPrivacySettings)