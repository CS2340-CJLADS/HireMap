from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "home"

# ============================================================================
# PRODUCTION 
# ============================================================================

from django.contrib.auth.decorators import login_required
from accounts.decorators import applicant_required, recruiter_required

PROD_DASHBOARD = login_required(TemplateView.as_view(template_name="home/dashboard.html"))
PROD_APPLICATIONS = applicant_required(TemplateView.as_view(template_name="home/applications_board.html"))
PROD_PROFILE = applicant_required(TemplateView.as_view(template_name="home/profile_edit.html"))
PROD_SAVED_SEARCHES = applicant_required(TemplateView.as_view(template_name="home/saved_searches.html"))
PROD_MESSAGES = applicant_required(TemplateView.as_view(template_name="home/messages_inbox.html"))
PROD_MAP = TemplateView.as_view(template_name="home/map.html")

prod_urlpatterns = [
    path("", views.index, name="index"),

    # Role dashboards (protected)
    path("dashboard/route/", views.dashboard_router, name="dashboard_router"),
    path("dashboard/applicant/", views.applicant_dashboard, name="applicant"),
    path("dashboard/recruiter/", views.recruiter_dashboard, name="recruiter"),

    # Protected TemplateViews
    path("dashboard/", PROD_DASHBOARD, name="dashboard"),
    path("applications/", PROD_APPLICATIONS, name="applications_board"),
    path("profile/", PROD_PROFILE, name="profile_edit"),
    path("saved-searches/", PROD_SAVED_SEARCHES, name="saved_searches"),
    path("messages/", PROD_MESSAGES, name="messages_inbox"),
    path("map/", PROD_MAP, name="map"),
]





# ============================================================================
# TESTING 
# Public access to all routes for easy manual testing
# ============================================================================

# Views rendered without auth/role requirements
# DASHBOARD = TemplateView.as_view(template_name="home/dashboard.html")
# APPLICATIONS = TemplateView.as_view(template_name="home/applications_board.html")
# PROFILE = TemplateView.as_view(template_name="home/profile_edit.html")
# SAVED_SEARCHES = TemplateView.as_view(template_name="home/saved_searches.html")
# MESSAGES = TemplateView.as_view(template_name="home/messages_inbox.html")
# MAP = TemplateView.as_view(template_name="home/map.html")

# urlpatterns = [
#     path("", views.index, name="index"),

#     # Role dashboards (still public during testing)
#     path("dashboard/route/", views.dashboard_router, name="dashboard_router"),
#     path("dashboard/applicant/", views.applicant_dashboard, name="applicant"),
#     path("dashboard/recruiter/", views.recruiter_dashboard, name="recruiter"),

#     # Public TemplateViews
#     path("dashboard/", DASHBOARD, name="dashboard"),
#     path("applications/", APPLICATIONS, name="applications_board"),
#     path("profile/", PROFILE, name="profile_edit"),
#     path("saved-searches/", SAVED_SEARCHES, name="saved_searches"),
#     path("messages/", MESSAGES, name="messages_inbox"),
#     path("map/", MAP, name="map"),
# ]



