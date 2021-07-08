from django.urls import path
from .views import RegisterAdmin


urlpatterns = [
    path('register', RegisterAdmin.as_view())
]