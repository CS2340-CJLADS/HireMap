from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.job_list, name="api_jobs_list"),
    path("jobs/<int:pk>/", views.job_detail, name="api_job_detail"),
]
