from django.urls import path
from .views import Contributor, Maintainer

urlpatterns = [
    path('contributor', Contributor.as_view()),
    path('maintainer', Maintainer.as_view())
]
