from threading import Thread

from apis import PostThrottle, check_token, service
from django.http.response import JsonResponse
from maintainer.utils import RequestSetPassword
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import AdminSchema, ApprovalSchema
from .perms import AuthAdminPerms
from .utils import (accepted_project_pagination, alpha_maintainer_support, beta_maintainer_support, project_pagination,
                    project_single_project)


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

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return JsonResponse(data={
                "error": "reCaptcha token not provided"
            }, status=401)

        if check_token(reCaptcha):

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
        return JsonResponse(data={
            "error": "Invalid recaptcha token"
        }, status=401)


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

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except Exception as e:
            return JsonResponse(data={
                "error": "reCaptcha token not provided"
            }, status=401)

        if check_token(reCaptcha):

            validate = AdminSchema(request.data).valid()
            if 'error' in validate:
                return JsonResponse(data={
                    "error": "Invalid data"
                }, status=400)
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
                return JsonResponse({"error": "ISR?"}, status=500)
            return JsonResponse(data={
                "error": "invalid password"
            }, status=401)

        return JsonResponse(data={
            "error": "Invalid recaptcha token"
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
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except Exception as e:
            return JsonResponse(data={
                "error": "recaptcha token not found"
            }, status=401)

        if check_token(reCaptcha):
            try:
                params = request.GET['role']
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

                if details := entry.find_maintainer_for_approval(validate.get(
                        'maintainer_id'), validate.get('project_id')):

                    project, maintainer = details

                    existing = entry.check_existing_maintainer(
                        email=validate.get('email')
                    )

                    if len(project['maintainer_id']) == 1:
                        response = alpha_maintainer_support(existing=existing, project=project,
                                                            maintainer=maintainer, request=request)
                        return JsonResponse(data=response.get("message"),
                                            status=response.get("status"))

                    if len(project['maintainer_id']) > 1:
                        response = beta_maintainer_support(existing=existing, project=project,
                                                           maintainer=maintainer, request=request)

                        return JsonResponse(data=response.get("message"), status=response.get("status"))

                return JsonResponse(data={
                    "error": "Invalid data / Maintainer already approved"
                }, status=400)

            elif params == 'project':
                if details := entry.approve_project(identifier=validate.get("project_id"),
                                                    project_url=validate.get(
                                                        "project_url"),
                                                    private=validate.get("private")):

                    project, maintainer = details
                    email_document = entry.get_all_maintainer_emails(
                        project=project)

                    email_document["email"].append(maintainer.pop("email"))
                    maintainer["name"] = "Maintainer(s)"
                    if service.wrapper_email(
                            role="project_approval", data={**project, **maintainer, **email_document}, send_all=True):
                        return JsonResponse(data={
                            "Approved Project": validate.get("project_id")
                        }, status=200)

                    entry.reset_status_project(project=project)
                    return JsonResponse(data={
                        "error": "Email failed"
                    }, status=500)

                return JsonResponse(data={
                    "error": "Inconsistant data"
                }, status=400)

            else:
                if details := entry.approve_contributor(project_id=validate.get("project_id"),
                                                        contributor_id=validate.get("contributor_id")):

                    contributor, project = details

                    if service.wrapper_email(
                            role="contributor_approval", data={
                                "name": contributor["name"],
                                "email": contributor["email"],
                                "project_name": project["project_name"],
                                "project_url": project["project_url"]
                            }):
                        return JsonResponse(data={
                            "admin_approved": True
                        }, status=200)

                    entry.reset_status_contributor(contributor=contributor)
                    return JsonResponse(data={
                        "error": "email not sent"
                    }, status=500)

                return JsonResponse(data={
                    "error": "contributor/project does not exist / contributor already approved"
                }, status=400)

        return JsonResponse(data={
            "error": "Invalid reCaptcha token"
        }, status=401)

    def get(self, request, **kwargs):

        Pagination = ['page']
        SingleProject = ['projectId', 'maintainer', 'contributor']
        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return project_pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_single_project(request, **kwargs)

        else:
            return JsonResponse({"error": "Query Params are different from expected"}, status=status.HTTP_400_BAD_REQUEST)


class AdminAccepted(APIView):
    def get(self, request, **kwargs) -> JsonResponse:
        """pagination for all accepted projects

        Args:
            request

        Returns:
            JsonResponse
        """
        if "page" not in request.GET:
            return JsonResponse({
                "error": "Invalid query paramerts"
            }, status=400)

        return accepted_project_pagination(request=request)
