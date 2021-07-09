from typing import Dict
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


def get_token(request_header: Dict[str, str]):
    try:
        token = request_header.get('Authorization').split()
        return token[0], token[1]
    except Exception as e:
        return False
