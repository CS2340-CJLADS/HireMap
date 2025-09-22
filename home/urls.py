from django.urls import path
from django.views.generic import TemplateView

app_name = "home"
HOME = TemplateView.as_view(template_name="home.html")
JOBS_LIST = TemplateView.as_view(template_name="jobs_list.html")
JOB_DETAIL = TemplateView.as_view(template_name="job_detail.html")
APPLICATIONS = TemplateView.as_view(template_name="applications_board.html")
PROFILE = TemplateView.as_view(template_name="profile_edit.html")
RECRUITER_JOBS = TemplateView.as_view(template_name="recruiter_jobs.html")
RECRUITER_JOB_NEW = TemplateView.as_view(template_name="recruiter_job_new.html")
SAVED_SEARCHES = TemplateView.as_view(template_name="saved_searches.html")
MESSAGES = TemplateView.as_view(template_name="messages_inbox.html")
MAP = TemplateView.as_view(template_name="map.html")

urlpatterns = [
    path("", HOME, name="index"),
    path("jobs/", JOBS_LIST, name="jobs_list"),
    path("jobs/<int:pk>/", JOB_DETAIL, name="job_detail"),
    path("applications/", APPLICATIONS, name="applications_board"),
    path("profile/", PROFILE, name="profile_edit"),
    path("recruiter/jobs/", RECRUITER_JOBS, name="recruiter_jobs"),
    path("recruiter/jobs/new/", RECRUITER_JOB_NEW, name="recruiter_job_new"),
    path("saved-searches/", SAVED_SEARCHES, name="saved_searches"),
    path("messages/", MESSAGES, name="messages_inbox"),
    path("map/", MAP, name="map"),
]
