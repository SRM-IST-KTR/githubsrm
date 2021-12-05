"""
URL configurations for GitHubSRM

"""
from django.urls import path, include, re_path
from apis.open_views import catch_all
from administrator.views import RefreshRoute
from administrator.views import Verification

urlpatterns = [
    path("api/", include("apis.urls")),
    path("admin/", include("administrator.urls")),
    path("maintainer/", include("maintainer.urls")),
    path("refresh-token", RefreshRoute.as_view()),
    path("me", Verification.as_view()),
    re_path("^(?P<path>.*)\/?$", catch_all),
]
