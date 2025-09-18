from django.contrib import admin

# Register your models here.
from .models import Applicant, Recruiter
admin.site.register(Applicant)
admin.site.register(Recruiter)