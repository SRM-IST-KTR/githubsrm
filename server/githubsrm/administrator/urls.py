from django.urls import path

from .views import ProjectsAdmin, admin_accepted, admin_login, register_admin

urlpatterns = [
    path("register", register_admin),
    path("projects", ProjectsAdmin.as_view()),
    path("projects/accepted", admin_accepted),
    path("login", admin_login),
]
