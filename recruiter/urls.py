from django.urls import path
from . import views

app_name = "recruiter"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("jobs/new/", views.job_new, name="job_new"),
    path("jobs/<int:job_id>/edit/", views.job_edit, name="job_edit"),
    path("jobs/<int:job_id>/delete/", views.job_delete, name="job_delete"),
    path("jobs/<int:job_id>/applications/", views.job_applications, name="job_applications"),
    path("applicants/<int:applicant_id>/", views.view_applicant, name="view_applicant"),
    path("search-candidates/", views.search_candidates, name="search_candidates"),
    path("get_applicant_info/<int:applicant_id>/", views.get_applicant_info, name="get_applicant_info"),
]
