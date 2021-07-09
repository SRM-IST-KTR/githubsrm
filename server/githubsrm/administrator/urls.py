from .views import ProjectsAdmin, RegisterAdmin, AdminLogin
from django.urls import path

urlpatterns = [
    path('register', RegisterAdmin.as_view()),
    path('projects', ProjectsAdmin.as_view()),
    path('login', AdminLogin.as_view())
]
