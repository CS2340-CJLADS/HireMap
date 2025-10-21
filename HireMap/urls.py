from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

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

    # User-specific apps
    path("recruiter/", include(("recruiter.urls", "recruiter"), namespace="recruiter")),
    path("seeker/", include(("seeker.urls", "seeker"), namespace="seeker")),

    # Home (shared pages)
    path("", include(("home.urls", "home"), namespace="home")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
