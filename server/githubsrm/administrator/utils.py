from rest_framework.views import APIView
from rest_framework import response, status


def project_Pagination(request, **kwargs):
    """
        Send paginated projects here
    """
    return response.Response(status=status.HTTP_200_OK)


def project_SingleProject(request, **kwargs):
    """
        Send single project but detailed
    """
    return response.Response(status=status.HTTP_200_OK)
