from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin first (and force /admin -> /admin/)
    path("admin/", admin.site.urls),
    path("admin", RedirectView.as_view(url="/admin/", permanent=False)),

    # API (server-rendered JSON)
    path("api/", include(("api.urls", "api"))),

    # Accounts (authentication)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Jobs
    path("jobs/", include(("jobs.urls", "jobs"), namespace="jobs")),

    # React SPA routes (explicit)
    path("", include(("home.urls", "home"), namespace="home")),
]
