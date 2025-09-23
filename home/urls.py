from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from accounts.decorators import applicant_required, recruiter_required
from . import views

app_name = "home"
DASHBOARD = login_required(TemplateView.as_view(template_name="dashboard.html"))
APPLICATIONS = applicant_required(TemplateView.as_view(template_name="applications_board.html"))
PROFILE = applicant_required(TemplateView.as_view(template_name="profile_edit.html"))
SAVED_SEARCHES = applicant_required(TemplateView.as_view(template_name="saved_searches.html"))
MESSAGES = applicant_required(TemplateView.as_view(template_name="messages_inbox.html"))
MAP = TemplateView.as_view(template_name="map.html")

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", DASHBOARD, name="dashboard"),
    path("applications/", APPLICATIONS, name="applications_board"),
    path("profile/", PROFILE, name="profile_edit"),
    path("saved-searches/", SAVED_SEARCHES, name="saved_searches"),
    path("messages/", MESSAGES, name="messages_inbox"),
    path("map/", MAP, name="map"),
]
