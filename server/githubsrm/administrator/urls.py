from .views import ProjectsAdmin, RegisterAdmin, AdminLogin, admin_accepted
from django.urls import path

urlpatterns = [
    path("register", RegisterAdmin.as_view()),
    path("projects", ProjectsAdmin.as_view()),
    path("projects/accepted", admin_accepted),
    path("login", AdminLogin.as_view()),
]
