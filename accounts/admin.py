from django.contrib import admin

# Register your models here.
from .models import Applicant, Recruiter, ApplicantPrivacySettings
admin.site.register(Applicant)
admin.site.register(Recruiter)
admin.site.register(ApplicantPrivacySettings)