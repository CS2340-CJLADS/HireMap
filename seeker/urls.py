from django.urls import path
from . import views

app_name = "seeker"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("applications/", views.applications, name="applications"),
    path("saved/", views.saved_jobs, name="saved_jobs"),
]
