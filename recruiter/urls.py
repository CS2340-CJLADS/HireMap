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
    
    # Saved searches and candidates
    path("saved-searches/", views.saved_searches, name="saved_searches"),
    path("save-search/", views.save_search, name="save_search"),
    path("saved-searches/<int:search_id>/delete/", views.delete_saved_search, name="delete_saved_search"),
    path("saved-searches/<int:search_id>/load/", views.load_saved_search, name="load_saved_search"),
    path("saved-candidates/", views.saved_candidates, name="saved_candidates"),
    path("save-candidate/<int:candidate_id>/", views.save_candidate, name="save_candidate"),
    path("unsave-candidate/<int:candidate_id>/", views.unsave_candidate, name="unsave_candidate"),
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/<int:notification_id>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("notifications/mark-all-read/", views.mark_all_notifications_read, name="mark_all_notifications_read"),
    path("notifications/<int:notification_id>/dismiss/", views.dismiss_notification, name="dismiss_notification"),
]
