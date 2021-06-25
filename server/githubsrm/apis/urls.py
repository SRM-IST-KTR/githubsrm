from django.urls import path
from .views import Contributor, Maintainer, HealthCheck

urlpatterns = [
    path('contributor', Contributor.as_view()),
    path('maintainer', Maintainer.as_view()),
    path('healthcheck', HealthCheck.as_view())
]
