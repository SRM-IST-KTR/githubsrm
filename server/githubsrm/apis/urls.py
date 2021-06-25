from django.urls import path
from .views import Contribute, Maintainer

urlpatterns = [
    path('contribute', Contribute.as_view()),
    path('maintainer', Maintainer.as_view())
]
