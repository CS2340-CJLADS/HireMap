from django.urls import path
from django.views.generic import TemplateView

app_name = "home"
SPA = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    path("", SPA, name="index"),
    path("jobs/", SPA, name="jobs_list"),
    path("jobs/<int:pk>/", SPA, name="job_detail"),
    path("applications/", SPA, name="applications_board"),
    path("profile/", SPA, name="profile_edit"),
    path("recruiter/jobs/", SPA, name="recruiter_jobs"),
    path("recruiter/jobs/new/", SPA, name="recruiter_job_new"),
    path("saved-searches/", SPA, name="saved_searches"),
    path("messages/", SPA, name="messages_inbox"),
    path("map/", SPA, name="map"),
]
