from django.shortcuts import render

from .utils import project_SingleProject, Projects_pagnation

from rest_framework import response, status
from rest_framework.views import APIView


# Create your views here.


class Projects(APIView):

    def get(self, request, **kwargs):

        Pagination = ['page']

        SingleProject = ['projectId', 'maintainer', 'contributor']

        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return response.Response(Projects_pagnation(request, **kwargs), status=status.HTTP_200_OK)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return response.Response(project_SingleProject(request, **kwargs), status=status.HTTP_200_OK)

        else:
            return response.Response("Query Params are different from expected", status=status.HTTP_400_BAD_REQUEST)
