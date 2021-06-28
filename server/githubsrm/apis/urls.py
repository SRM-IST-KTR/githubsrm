from django.urls import path
from .open_views import (
    Contributor, Maintainer, HealthCheck, Team, ContactUs
)
from .admin_views import AdminContributor, AdminMaintainer

urlpatterns = [
    path('contributor', Contributor.as_view()),
    path('maintainer', Maintainer.as_view()),
    path('healthcheck', HealthCheck.as_view()),
    path('team', Team.as_view()),
    path('contact-us', ContactUs.as_view()),
    path('admin/contributor', AdminContributor.as_view()),
    path('admin/maintainer', AdminMaintainer.as_view())
]
