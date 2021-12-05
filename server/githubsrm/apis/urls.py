from django.urls import path
from .open_views import Contributor, Maintainer, HealthCheck, Team, ContactUs


urlpatterns = [
    path("contributor", Contributor.as_view()),
    path("maintainer", Maintainer.as_view()),
    path("healthcheck", HealthCheck.as_view()),
    path("team", Team.as_view()),
    path("contact-us", ContactUs.as_view()),
]
