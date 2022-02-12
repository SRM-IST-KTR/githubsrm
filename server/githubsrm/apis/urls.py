from django.urls import path

from .open_views import ContactUs, Contributor, Maintainer, team

urlpatterns = [
    path("contributor", Contributor.as_view()),
    path("maintainer", Maintainer.as_view()),
    path("contact-us", ContactUs.as_view()),
    path("team", team),
]
