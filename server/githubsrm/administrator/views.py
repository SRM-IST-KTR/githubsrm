
from json.encoder import JSONEncoder
import re
from threading import Thread
from apis import PostThrottle, check_token, service
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import (
    AdminSchema, ApprovalSchema, RejectionSchema
)
from .perms import AuthAdminPerms
from .utils import (
    accepted_project_pagination, alpha_maintainer_support,
    beta_maintainer_support, get_token, project_pagination,
    project_single_project
)


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
                        'maintainer_id'), validate.get('project_id'), validate.get("email")):

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
                        alpha_email = entry.get_maintainer_email(
                            identifier=project["maintainer_id"][0])
                        response = beta_maintainer_support(existing=existing, project=project,
                                                           maintainer=maintainer, alpha_email=alpha_email,
                                                           request=request)

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
                    if email_document:
                        email_document["email"].append(maintainer.pop("email"))
                        if service.wrapper_email(
                                role="project_approval", data={**{
                                    "name": "Maintainer(s)",
                                    "project_name": project["project_name"],
                                    "project_url": validate["project_url"],
                                    "project_id": project["_id"]

                                }, **email_document}, send_all=True):
                            return JsonResponse(data={
                                "Approved Project": validate.get("project_id")
                            }, status=200)
                    else:
                        entry.reset_status_project(project=project)

                        blame = None
                        try:
                            if decoded := jwt_keys.verify_key(request.headers.get("Authorization").split()[1]):
                                blame = decoded.get("user")
                        except Exception as e:
                            blame = None

                        Thread(target=service.sns, kwargs={"payload": {
                            "message": "Trying to approve project without approving maintainers",
                            "subject": f"[ADMIN-ERROR] This person messed up -> {blame}"
                        }}).start()

                        return JsonResponse(data={
                            "error": "Approve maintainer before approving project"
                        }, status=400)

                    entry.reset_status_project(project=project)
                    return JsonResponse(data={
                        "error": "email failed"
                    }, status=500)

                return JsonResponse(data={
                    "error": "Inconsistant data"
                }, status=400)

            else:
                if details := entry.approve_contributor(project_id=validate.get("project_id"),
                                                        contributor_id=validate.get("contributor_id")):

                    contributor, project = details
                    emails = entry.get_all_maintainer_emails(project=project)
                    Thread(target=service.wrapper_email, kwargs={
                        "role": "contributor_application_to_maintainer",
                        "send_all": True,
                        "data": {
                            "name": "Maintainer(s)",
                            "project_name": project["project_name"],
                            "contributor_name": contributor["name"],
                            "contributor_email": contributor["email"],
                            "email": emails["email"]
                        }}).start()

                    return JsonResponse(data={
                        "admin_approved": True
                    }, status=200)

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

    @staticmethod
    def _remove_contributor(request) -> JsonResponse:
        """Send sns of contributor removal with blame

        Returns:
            JsonResponse
        """

        key = jwt_keys.verify_key(get_token(request.headers))

        Thread(target=service.sns, kwargs={
            "payload": {
                "message": f"Contributor -> {request.data.get('contributor_id')} removed by -> {key.get('user')}",
                "subject": "[CONTRIBUTOR-REMOVE]"
            }
        }).start()
        return JsonResponse(data={
            "removed": str(request.data.get("contributor_id"))
        }, status=200)

    @staticmethod
    def _remove_maintainer(request) -> JsonResponse:
        """Send sns of maintianer removal with blame

        Args:
            request

        Returns:
            JsonResponse
        """
        key = jwt_keys.verify_key(get_token(request.headers))
        Thread(target=service.sns, kwargs={
            "payload": {
                "message": f"Maintainer -> {request.data.get('maintainer_id')} removed by -> {key.get('user')}",
                "subject": "[MAINTAINER-REMOVAL]"
            }
        }).start()

        return JsonResponse(data={
            "removed": str(request.data.get("maintainer_id"))
        }, status=200)

    @staticmethod
    def _error_maintainer(request) -> JsonResponse:
        """Warning sns

        Args:
            request

        Returns:
            JsonResponse
        """
        key = jwt_keys.verify_key(get_token(request.headers))
        Thread(target=service.sns, kwargs={
            "payload": {
                "message": f"This admin messed up -> {key.get('user')} \
                trying to remove admin approved maintainer({request.data.get('maintainer_id')})",
                "subject": "[WARNING-ADMIN-MESSED-UP]"
            }
        }).start()

        return JsonResponse(data={
            "error": "Invalid request"
        }, status=400)

    @staticmethod
    def _error_contributor(request) -> JsonResponse:
        """Warning sns

        Args:
            request

        Returns:
            JsonResponse
        """
        key = jwt_keys.verify_key(get_token(request.headers))
        Thread(target=service.sns, kwargs={
            "payload": {
                "message": f"Tring to remove maintainer / admin or the contributor id is wrong\
                     approved contributor ({request.data.get('contributor_id')}), {key.get('user')} messed up.",
                "subject": "[WARNING-ADMIN-MESSED-UP]"
            }
        }).start()

        return JsonResponse(data={
            "error": "invalid request"
        }, status=400)

    def action_to_status(self, status: str, request) -> None:
        """Take action according to the response from remove functions

        Args:
            status (str): response
            request:  blame
        """

        if request.GET.get("role") == "contributor":
            if status:
                return self._remove_contributor(reqeust=request)
            else:
                return self._error_contributor(request=request)
        else:
            if status:
                return self._remove_maintainer(request=request)
            else:
                return self._error_maintainer(request=request)

    def delete(self, request, **kwargs) -> JsonResponse:
        """Delete route for admin rejections

        Args:
            request

        Returns:
            JsonResponse
        """
        try:
            recaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return JsonResponse(data={
                "error": "token not provided"
            }, status=401)

        if check_token(recaptcha):
            validate = RejectionSchema(
                data=request.data, params=request.GET.get("role")).valid()
            if "error" in validate:
                return JsonResponse(data={
                    "error": validate.get("error")
                }, status=400)

            else:
                if request.GET.get("role") == "contributor":
                    remove_status = entry.admin_remove_contributor(
                        validate.get("contributor_id"))
                    return self.action_to_status(
                        status=remove_status, request=request)
                else:
                    remove_status = entry.admin_remove_maintainer(
                        validate.get("maintainer_id"))
                    return self.action_to_status(
                        status=remove_status, request=request)
        else:
            return JsonResponse(data={
                "error": "invalid recaptcha token"
            }, status=401)


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
