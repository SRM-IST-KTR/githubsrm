from django.urls import path
from .views import Contribute

urlpatterns = [
    path('contribute', Contribute.as_view())
]
