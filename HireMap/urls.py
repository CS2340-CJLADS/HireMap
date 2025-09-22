from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView

SPA = TemplateView.as_view(template_name="index.html")

urlpatterns = [
    # Admin FIRST (and /admin -> /admin/)
    path("admin/", admin.site.urls),
    path("admin", RedirectView.as_view(url="/admin/", permanent=False)),

    # API
    path("api/", include(("api.urls", "api"))),

    # SPA routes
    path("", include(("home.urls", "home"), namespace="home")),

    # Catch-all for front-end routes, EXCEPT server prefixes
    re_path(r"^(?!admin/|api/|static/|media/).*$", SPA),
]
