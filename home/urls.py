from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "home"
DASHBOARD = TemplateView.as_view(template_name="dashboard.html")
APPLICATIONS = TemplateView.as_view(template_name="applications_board.html")
PROFILE = TemplateView.as_view(template_name="profile_edit.html")
SAVED_SEARCHES = TemplateView.as_view(template_name="saved_searches.html")
MESSAGES = TemplateView.as_view(template_name="messages_inbox.html")
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
