"""
URL configurations for GitHubSRM

"""
from administrator.views import RefreshRoute, Verification
from apis.open_views import catch_all
from django.urls import include, path, re_path

from .views import health_check

urlpatterns = [
    path("api/", include("apis.urls")),
    path("admin/", include("administrator.urls")),
    path("maintainer/", include("maintainer.urls")),
    path("refresh-token", RefreshRoute.as_view()),
    path("me", Verification.as_view()),
    path("api/healthcheck", health_check),
    re_path("^(?P<path>.*)\/?$", catch_all),
]
