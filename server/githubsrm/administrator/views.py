
from rest_framework import response, status
from rest_framework.views import APIView
from rest_framework import response, status
from administrator import jwt_keys, entry
from .utils import project_SingleProject, project_Pagination


from .definitions import AdminSchema
from .perms import RegisterAdminPerms


class RegisterAdmin(APIView):
    permission_classes = [RegisterAdminPerms]

    def post(self, request, **kwargs):
        """Register Admins

        Args:
            request
        """
        valid = AdminSchema(request.data).valid()

        if 'error' in valid:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        if entry.insert_admin(request.data):
            return response.Response(data={
                "registered": True
            }, status=status.HTTP_200_OK)
        return response.Response(data={
            "invalid data / user exists"
        }, status=status.HTTP_400_BAD_REQUEST)


class AdminLogin(APIView):
    """
    Log in admins.
    """

    def post(self, request, **kwargs) -> response.Response:
        """Handle post data on this route and issue jwtkeys.

        Args:
            request

        Returns:
            response.Response: [description]
        """
        validate = AdminSchema(request.data).valid()
        if 'error' in validate:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        password = validate.get('password')
        if entry.verify_admin(email=validate.get('email'), password=password):
            keys = jwt_keys.issue_key(payload={
                "admin": True,
                "user": validate.get('email')
            })

            if keys:
                return response.Response(data={
                    "keys": keys
                }, status=status.HTTP_200_OK)
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response(data={
            "error": "invalid password"
        }, status=status.HTTP_401_UNAUTHORIZED)


class ProjectsAdmin(APIView):

    def post(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):

        Pagination = ['page']

        SingleProject = ['projectId', 'maintainer', 'contributor']

        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return project_Pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_SingleProject(request, **kwargs)

        else:
            return response.Response("Query Params are different from expected",status=status.HTTP_400_BAD_REQUEST)
