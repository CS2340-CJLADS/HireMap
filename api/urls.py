from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.jobs_list, name="api.jobs_list"),
    path("jobs/<int:pk>/", views.job_detail, name="api.job_detail"),
    path("applications/<int:pk>/status/", views.update_application_status, name="api.update_application_status"),
    path("recruiter/board/", views.recruiter_board, name="api.recruiter_board"),
]
