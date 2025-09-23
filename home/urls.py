from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "home"


# ============================================================================
# TESTING 
# Public access to all routes for easy manual testing
# ============================================================================

# Views rendered without auth/role requirements
PROFILE = TemplateView.as_view(template_name="home/profile_edit.html")
SAVED_SEARCHES = TemplateView.as_view(template_name="home/saved_searches.html")
MESSAGES = TemplateView.as_view(template_name="home/messages_inbox.html")
MAP = TemplateView.as_view(template_name="home/map.html")
RECRUITER_APPLICANTS = TemplateView.as_view(template_name="home/recruiter_applicants.html")
JOB_SEARCH = TemplateView.as_view(template_name="home/job_search.html")
JOB_DETAILS = TemplateView.as_view(template_name="home/job_details.html")
MANAGE_JOBS = TemplateView.as_view(template_name="home/manage_jobs.html")
POST_JOB = TemplateView.as_view(template_name="home/post_job.html")
EDIT_JOB = TemplateView.as_view(template_name="home/edit_job.html")
SEARCH_CANDIDATES = TemplateView.as_view(template_name="home/search_candidates.html")

urlpatterns = [
    path("", views.index, name="index"),

    # Role dashboards (still public during testing)
    path("dashboard/route/", views.dashboard_router, name="dashboard_router"),
    path("dashboard/applicant/", views.applicant_dashboard, name="applicant"),
    path("dashboard/recruiter/", views.recruiter_dashboard, name="recruiter"),
    path("dashboard/recruiter/applicants/", RECRUITER_APPLICANTS, name="recruiter_applicants"),  # legacy/testing path
    path("applicants/", RECRUITER_APPLICANTS, name="recruiter_applicants_short"),

    # Public TemplateViews (no generic /dashboard route)
    path("profile/", PROFILE, name="profile_edit"),
    path("saved-searches/", SAVED_SEARCHES, name="saved_searches"),
    path("messages/", MESSAGES, name="messages_inbox"),
    path("map/", MAP, name="map"),
    
    # Job-related pages
    path("job-search/", JOB_SEARCH, name="job_search"),
    path("jobs/<int:job_id>/", JOB_DETAILS, name="job_details"),
    path("manage-jobs/", MANAGE_JOBS, name="manage_jobs"),
    path("post-job/", POST_JOB, name="post_job"),
    path("edit-job/", EDIT_JOB, name="edit_job"),
    path("search-candidates/", SEARCH_CANDIDATES, name="search_candidates"),
]



