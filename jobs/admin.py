from django.contrib import admin
from .models import Job

<<<<<<< Updated upstream
# Register your models here.
from .models import JobPosting
admin.site.register(JobPosting)
=======
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "work_type", "created_at")
    list_filter = ("work_type", "created_at")
    search_fields = ("title", "company", "location", "skills", "summary", "description")
    fieldsets = (
        ("Basics", {"fields": ("title", "company", "location", "work_type", "salary", "skills", "summary")}),
        ("Details", {"fields": ("description", "responsibilities", "qualifications")}),
        ("Map", {"fields": ("lat", "lng")}),
    )
>>>>>>> Stashed changes
