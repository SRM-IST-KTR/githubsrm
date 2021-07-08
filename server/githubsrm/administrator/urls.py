from .views import ProjectsAdmin, RegisterAdmin
from django.urls import path

urlpatterns = [
    path('register', RegisterAdmin.as_view()),
    path('projects', ProjectsAdmin.as_view())
]
