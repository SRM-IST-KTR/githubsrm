from django.urls import path

from .open_views import Contributor, Maintainer, contact_us, team

urlpatterns = [
    path("contributor", Contributor.as_view()),
    path("maintainer", Maintainer.as_view()),
    path("contact-us", contact_us),
    path("team", team),
]
