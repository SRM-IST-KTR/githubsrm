
from apis import service
from apis import PostThrottle
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
            return JsonResponse(data={
                "error": valid
            }, status=400)

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

                existing = entry.check_existing_maintainer(
                    identifier=validate.get('maintainer_id')
                )

                if len(value['maintainer_id']) == 1:
                    #! Alpha maintainer flow
                    if existing:
                        # ? service.wrapper_email() send conformation emails.
                        return JsonResponse(data={
                            "success": "Approved existing maintainer"
                        }, status=200)
                    else:
                        password = entry.get_random_password(
                            identifier=validate.get("maintainer_id"))
                        print(password)

                        # ? service.wrapper_email() send conformation emails with password.
                        return JsonResponse(data={
                            "success": "Approved new maintainer"
                        }, status=200)

                if len(value['maintainer_id']) > 1:
                    #! Beta maintainer flow
                    if existing:
                        # ? service.wrapper_email send acceptance email to beta maintainer
                        # ? Alpha maintainer gets an email of beta maintainer's approval
                        return JsonResponse(data={
                            "Approved existing maintainer": True
                        }, status=200)

                    else:
                        password = entry.get_random_password(
                            identifier=validate.get("maintainer_id"))
                        # ? service.wrappe_email send acceptance email to beta maintainer with password
                        # ? Alpha maintainer gets an email of beta maintainer's approval
                        print(password)
                        return JsonResponse(data={
                            "Approved new maintainer": True
                        }, status=200)

            return JsonResponse(data={
                "error": "Invalid data / Maintainer already approved"
            }, status=400)

        elif params == 'project':
            if entry.approve_project(identifier=validate.get("project_id"),
                                     project_url=validate.get("project_url"),
                                     private=validate.get("private")):

                # ? service.wrapper send maintainer approval conformation
                return JsonResponse(data={
                    "Approved Project": validate.get("project_id")
                }, status=200)
            return JsonResponse(data={
                "error": "Inconsistant data"
            }, status=400)

        else:
            if entry.approve_contributor(project_id=validate.get("project_id"),
                                         contributor_id=validate.get("contributor_id")):

                return JsonResponse(data={
                    "admin_approved": True
                }, status=200)

            return JsonResponse(data={
                "error": "contributor/project does not exist / contributor already approved"
            }, status=400)

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
