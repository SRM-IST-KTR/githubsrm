from .views import Projects, Login
from django.urls import path


urlpatterns = [
    path('projects', Projects.as_view()),
    path('login', Login.as_view())
]
