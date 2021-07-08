from django.urls import path
from .views import RegisterAdmin, ProjectsAdmin


urlpatterns = [
    path('register', RegisterAdmin.as_view()),
    path('projects', ProjectsAdmin.as_view())
]
