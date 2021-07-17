from .views import Projects, Login, ResetPassword, SetPassword
from django.urls import path


urlpatterns = [
    path('projects', Projects.as_view()),
    path('login', Login.as_view()),
    path('reset-password', ResetPassword.as_view()),
    path('set-password', SetPassword.as_view())
]
