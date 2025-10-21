from django.urls import path
from django.views.generic import TemplateView, RedirectView
from . import views

app_name = "home"


# ============================================================================
# TESTING 
# Public access to all routes for easy manual testing
# ============================================================================

# Only keep functional pages

# Accounts pages
ACCOUNTS_INDEX = TemplateView.as_view(template_name="accounts/index.html")
ACCOUNTS_SIGNUP = TemplateView.as_view(template_name="accounts/signup.html")
ACCOUNTS_LOGIN = TemplateView.as_view(template_name="accounts/login.html")

urlpatterns = [
    # Redirect to appropriate dashboard based on user type
    path("", RedirectView.as_view(url="/seeker/", permanent=False), name="index"),
    
    # Redirect old routes to new structure
    path("job-search/", RedirectView.as_view(url="/seeker/", permanent=False), name="job_search_dashboard"),
    path("my-applications/", RedirectView.as_view(url="/seeker/applications/", permanent=False), name="my_applications"),
    path("profile/", RedirectView.as_view(url="/seeker/profile/", permanent=False), name="profile"),
    
    # Accounts pages (no login required)
    path("accounts/", ACCOUNTS_INDEX, name="accounts_index"),
    path("accounts/signup/", ACCOUNTS_SIGNUP, name="accounts_signup"),
    path("accounts/login/", ACCOUNTS_LOGIN, name="accounts_login"),
    
    # Redirect old routes to new structure
    path("jobs/", RedirectView.as_view(url="/seeker/", permanent=False), name="jobs_index"),
    path("jobs/my-applications/", RedirectView.as_view(url="/seeker/applications/", permanent=False), name="jobs_my_applications"),
    path("jobs/profile/edit/", RedirectView.as_view(url="/seeker/profile/", permanent=False), name="jobs_profile_redirect"),
    path("applications/", RedirectView.as_view(url="/seeker/applications/", permanent=False), name="applications_board"),
    
    # Candidate search for recruiters
    path("search-candidates/", views.search_candidates, name="search_candidates"),
]



