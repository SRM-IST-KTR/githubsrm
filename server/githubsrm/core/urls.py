"""
URL configurations for GitHubSRM

"""
from django.contrib import admin
from django.urls import path, include, re_path
from apis.open_views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls')),
    re_path('^(?P<path>.*)/?\/$', home),
    path('', home)
]
