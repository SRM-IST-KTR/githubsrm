from .views import Projects, login, reset_password, set_password
from django.urls import path


urlpatterns = [
    path("projects", Projects.as_view()),
    path("login", login),
    path("reset-password/reset", reset_password),
    path("reset-password/set", set_password),
]
