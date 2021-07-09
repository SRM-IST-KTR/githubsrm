from .views import Projects
from django.urls import path


urlpatterns = [
    path('projects', Projects.as_view()),
]
