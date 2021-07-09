
from apis.throttle import PostThrottle
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import AdminSchema
from .perms import AuthAdminPerms
from .utils import project_Pagination, project_SingleProject


class RegisterAdmin(APIView):
    permission_classes = [AuthAdminPerms]
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Register Admins

        Args:
            request

        Returns:
            JsonResponse
        """
        valid = AdminSchema(request.data).valid()

        if 'error' in valid:
            return JsonResponse(status=400)

        if entry.insert_admin(request.data):
            return JsonResponse(data={
                "registered": True
            }, status=200)
        return JsonResponse(data={
            "error":"invalid data / user exists"
        }, status=status.HTTP_400_BAD_REQUEST)


class AdminLogin(APIView):
    """
    Log in admins.
    """
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Handle post data on this route and issue jwtkeys.

        Args:
            request

        Returns:
            response.Response: [description]
        """
        validate = AdminSchema(request.data).valid()
        if 'error' in validate:
            return JsonResponse(status=400)
        password = validate.get('password')
        if entry.verify_admin(email=validate.get('email'), password=password):
            keys = jwt_keys.issue_key(payload={
                "admin": True,
                "user": validate.get('email')
            })

            if keys:
                return JsonResponse(data={
                    "keys": keys
                }, status=200)
            return JsonResponse(status=500)
        return JsonResponse(data={
            "error": "invalid password"
        }, status=401)


class ProjectsAdmin(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs):
        return JsonResponse(status=status.HTTP_200_OK)

    def get(self, request, **kwargs):

        Pagination = ['page']

        SingleProject = ['projectId', 'maintainer', 'contributor']

        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return project_Pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_SingleProject(request, **kwargs)

        else:
            return JsonResponse({"error":"Query Params are different from expected"}, status=status.HTTP_400_BAD_REQUEST)
