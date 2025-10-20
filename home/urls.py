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
    # Main functional pages
    path("", views.job_search_dashboard, name="index"),  # Redirect home to job search
    path("job-search/", views.job_search_dashboard, name="job_search_dashboard"),
    path("my-applications/", views.my_applications, name="my_applications"),
    
    # Accounts pages (no login required)
    path("accounts/", ACCOUNTS_INDEX, name="accounts_index"),
    path("accounts/signup/", ACCOUNTS_SIGNUP, name="accounts_signup"),
    path("accounts/login/", ACCOUNTS_LOGIN, name="accounts_login"),
    
    # Redirect old routes to functional pages
    path("jobs/", RedirectView.as_view(url="/job-search/", permanent=False), name="jobs_index"),
    path("jobs/my-applications/", RedirectView.as_view(url="/my-applications/", permanent=False), name="jobs_my_applications"),
    path("applications/", RedirectView.as_view(url="/my-applications/", permanent=False), name="applications_board"),
]



