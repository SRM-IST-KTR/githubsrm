
from rest_framework.views import APIView
from .perms import CustomPerms
from .models import Entry
from rest_framework import response, status
from .definitions import AdminSchema

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
        valid = AdminSchema(data=request.data, headers={
            "path_info": request.path_info
        }, method='PUT').valid()

        if 'error' not in valid:
            result = entry.approve_contributor(identifier=valid.get(
                'contributor_id'), project_id=valid.get('project_id'))
            if result:
                return response.Response(data={
                    "approved": f"{request.data.get('contributor_id')}"
                }, status=status.HTTP_200_OK)
            return response.Response(data={
                "invalid id": request.data
            }, status=status.HTTP_400_BAD_REQUEST)

        return response.Response({
            "invalid data": request.data,
            "error": valid.get('error')
        })


class AdminMaintainer(APIView):
    """Admin routes for maintainer

    Args:
        APIView 
    """
    permission_classes = [CustomPerms]
