
from rest_framework.views import APIView
from .perms import CustomPerms
from .models import Entry
from rest_framework import response, status


entry = Entry()


class AdminContributor(APIView):
    """Admin routes for contributor

    Args:
        APIView 
    """
    permission_classes = [CustomPerms]

    def put(self, request, **kwargs) -> response.Response:
        """To approve contributos

        Args:
            request

        Returns:
            response.Response
        """
        pass
        

class AdminMaintainer(APIView):
    """Admin routes for maintainer

    Args:
        APIView 
    """
    permission_classes = [CustomPerms]
    pass