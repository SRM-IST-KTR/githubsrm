
from django.http import response
from apis import service
from apis.throttle import PostThrottle
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import AdminSchema, ApprovalSchema
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
            "error": "invalid data / user exists"
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
            JsonResponse 
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

    def post(self, request, **kwargs) -> JsonResponse:
        """Handle Approval of maintainer, contributor and Project. 

        Args:
            request ([type])

        Returns:
            JsonResponse
        """
        try:
            params = request.GET.get('role')
        except Exception as e:
            return JsonResponse(data={
                "error": "invalid query parameters"
            }, status=400)

        validate = ApprovalSchema(request.data, params=params).valid()
        if 'error' in validate:
            return JsonResponse(data={
                "error": str(validate.get('error'))
            }, status=400)
        if params == 'maintainer':

            if value := entry.find_maintainer_for_approval(validate.get(
                    'maintainer_id'), validate.get('project_id')):

                try:
                    if len(value['maintainer_id']) == 1:
                        #! Alpha maintainer flow
                        if entry.check_existing_maintainer(
                            identifier=validate.get('maintainer_id')
                        ):
                            # ? service.wrapper_email() send conformation emails.
                            return JsonResponse(data={
                                "success": "Approved existing maintainer"
                            }, status=200)
                        else:
                            password = entry.get_random_password(
                                identifier=validate.get("maintainer_id"))
                             # ? service.wrapper_email() send conformation emails with password.
                            return JsonResponse(data={
                                "success": "Approved new maintainer"
                            }, status=200)

                    if len(value['maintainer_id']) > 1:
                        #! Follow beta maintainer
                        print("FOLLOW BETA")

                except Exception as e:
                    print(e)
                    return JsonResponse(data={
                        "error": str(e)
                    }, status=400)

            return JsonResponse(data={
                "error": "Invalid data / Maintainer already approved"
            }, status=400)

        return JsonResponse(data={}, status=status.HTTP_200_OK)

    #! Requires formatting.
    def get(self, request, **kwargs):

        Pagination = ['page']
        SingleProject = ['projectId', 'maintainer', 'contributor']
        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return project_Pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_SingleProject(request, **kwargs)

        else:
            return JsonResponse({"error": "Query Params are different from expected"}, status=status.HTTP_400_BAD_REQUEST)
