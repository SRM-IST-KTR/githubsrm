"""
URL configurations for GitHubSRM

"""
from administrator.views import refresh, verify
from apis.open_views import catch_all
from django.urls import include, path, re_path

from .views import health_check

urlpatterns = [
    path("api/", include("apis.urls")),
    path("admin/", include("administrator.urls")),
    path("maintainer/", include("maintainer.urls")),
    path("refresh-token", refresh),
    path("me", verify),
    path("api/healthcheck", health_check),
    re_path("^(?P<path>.*)\/?$", catch_all),
]
