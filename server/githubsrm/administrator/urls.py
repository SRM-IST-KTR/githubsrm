from .views import ProjectsAdmin, RegisterAdmin, AdminLogin, AdminAccepted
from django.urls import path

urlpatterns = [
    path("register", RegisterAdmin.as_view()),
    path("projects", ProjectsAdmin.as_view()),
    path("projects/accepted", AdminAccepted.as_view()),
    path("login", AdminLogin.as_view()),
]
