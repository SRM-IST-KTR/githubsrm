from .views import (
    Projects, Login, ResetPassword, SetPassword,
    RefreshRoute, Verification
)
from django.urls import path


urlpatterns = [
    path('projects', Projects.as_view()),
    path('login', Login.as_view()),
    path('reset-password/reset', ResetPassword.as_view()),
    path('reset-password/set', SetPassword.as_view()),
    path("refresh-token", RefreshRoute.as_view()),
    path("me", Verification.as_view())
]
