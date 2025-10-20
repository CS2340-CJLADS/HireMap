from django.urls import path
from django.views.generic import TemplateView, RedirectView
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
    path("profile/", views.profile_view, name="profile_edit"),
    path("recruiter-profile/", views.recruiter_profile_view, name="recruiter_profile"),
    path("recruiter-profile/edit/", views.recruiter_profile_edit, name="recruiter_profile_edit"),
    path("saved-searches/", SAVED_SEARCHES, name="saved_searches"),
    path("messages/", MESSAGES, name="messages_inbox"),
    path("map/", MAP, name="map"),
    path("applications/", RedirectView.as_view(url="/jobs/my-applications/", permanent=False), name="applications_board"),
    
    # Job-related pages (redirect to proper jobs app)
    path("job-search/", views.job_search_dashboard, name="job_search_dashboard"),
    path("jobs/<int:job_id>/", RedirectView.as_view(url="/jobs/%(job_id)s/", permanent=False), name="job_details"),
    path("manage-jobs/", RedirectView.as_view(url="/jobs/recruiter/jobs/", permanent=False), name="manage_jobs"),
    path("post-job/", RedirectView.as_view(url="/jobs/recruiter/jobs/new/", permanent=False), name="post_job"),
    path("edit-job/", RedirectView.as_view(url="/jobs/recruiter/jobs/1/edit/", permanent=False), name="edit_job"),
    path("search-candidates/", views.search_candidates, name="search_candidates"),
]



