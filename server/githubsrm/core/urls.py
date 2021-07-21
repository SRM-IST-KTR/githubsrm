"""
URL configurations for GitHubSRM

"""
from django.urls import path, include, re_path
from apis.open_views import catch_all

urlpatterns = [
    path('api/', include('apis.urls')),
    path('admin/', include('administrator.urls')),
    path('maintainer/', include('maintainer.urls')),
    re_path('^(?P<path>.*)\/?$', catch_all),
]
