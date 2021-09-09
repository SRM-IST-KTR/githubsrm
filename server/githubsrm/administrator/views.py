from threading import Thread

from core import service
from core.errorfactory import (
    AuthenticationErrors,
    ProjectErrors,
    ContributorErrors,
    MaintainerErrors,
)
from core.settings import PostThrottle
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import AdminSchema, ApprovalSchema, RejectionSchema
from .errors import ExistingAdminError, InvalidAdminCredentialsError
from .perms import AuthAdminPerms
from .utils import (
    accepted_project_pagination, alpha_maintainer_support,
    beta_maintainer_support, get_token, project_pagination,
    project_single_project
)
from .models import (
    hash_password,
    check_hash
)

maintainer_entry = Entry()


class RegisterAdmin(APIView):
    permission_classes = [AuthAdminPerms]
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Register Admins

        Args:
            request: request object

        Returns:
            JsonResponse: status
        """

        valid = AdminSchema(request.data).valid()
        if "error" in valid:
            return JsonResponse(data={"error": valid}, status=400)
        try:
            entry.insert_admin(request.data)
            return JsonResponse(data={"registred": True}, status=200)
        except ExistingAdminError as e:
            return JsonResponse(data={"error": str(e)}, status=400)


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
        if "error" in validate:
            return JsonResponse(data={"error": "Invalid data"}, status=400)
        password = validate.get("password")
        try:
            entry.verify_admin(email=validate.get("email"), password=password)
            keys = jwt_keys.issue_key(
                payload={"admin": True, "user": validate.get("email")},
                get_refresh_token=True,
            )
            return JsonResponse(data=keys, status=200)
        except InvalidAdminCredentialsError as e:
            return JsonResponse(data={"error": str(e)}, status=401)


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
            params = request.GET["role"]
        except Exception as e:
            return JsonResponse(data={"error": "invalid query parameters"}, status=400)

        validate = ApprovalSchema(request.data, params=params).valid()
        if "error" in validate:
            return JsonResponse(data={"error": str(validate.get("error"))}, status=400)
        if params == "maintainer":

            try:
                project, maintainer = entry.find_maintainer_for_approval(
                    validate.get("maintainer_id"),
                    validate.get("project_id"),
                    validate.get("email"),
                )
                existing = entry.check_existing_maintainer(email=validate.get("email"))

                if len(project["maintainer_id"]) == 1:
                    response = alpha_maintainer_support(
                        existing=existing,
                        project=project,
                        maintainer=maintainer,
                        request=request,
                    )
                    return JsonResponse(
                        data=response.get("message"), status=response.get("status")
                    )

                if len(project["maintainer_id"]) > 1:
                    alpha_email = entry.get_maintainer_email(
                        identifier=project["maintainer_id"][0]
                    )
                    response = beta_maintainer_support(
                        existing=existing,
                        project=project,
                        maintainer=maintainer,
                        alpha_email=alpha_email,
                        request=request,
                    )

                    return JsonResponse(
                        data=response.get("message"), status=response.get("status")
                    )
            except MaintainerErrors as e:
                return JsonResponse(data={"error": str(e)}, status=400)

        elif params == "project":
            try:
                project = entry.approve_project(
                    identifier=validate.get("project_id"), year=validate.get("year")
                )
                email_document = entry.get_all_maintainer_emails(project=project)
                if email_document:
                    if service.wrapper_email(
                        role="project_approval",
                        data={
                            **{
                                "name": "Maintainer(s)",
                                "project_name": project["project_name"],
                                "project_url": project["project_url"],
                                "project_id": project["_id"],
                            },
                            **email_document,
                        },
                        send_all=True,
                    ):
                        return JsonResponse(
                            data={"Approved Project": validate.get("project_id")},
                            status=200,
                        )
                    entry.reset_status_project(project=project)
                    return JsonResponse(data={"error": "email failed"}, status=500)
                else:
                    entry.reset_status_project(project=project)

                    blame = None
                    try:
                        blame = request.decoded.get("user")
                    except Exception as e:
                        blame = None

                    Thread(
                        target=service.sns,
                        kwargs={
                            "payload": {
                                "message": "Trying to approve project without approving maintainers",
                                "subject": f"[ADMIN-ERROR] This person messed up -> {blame}",
                            }
                        },
                    ).start()

                    return JsonResponse(
                        data={"error": "Approve maintainer before approving project"},
                        status=400,
                    )
            except ProjectErrors as e:
                return JsonResponse(data={"error": str(e)}, status=400)

        else:
            try:
                contributor, project = entry.approve_contributor(
                    project_id=validate.get("project_id"),
                    contributor_id=validate.get("contributor_id"),
                )

                emails = entry.get_all_maintainer_emails(project=project)
                Thread(
                    target=service.wrapper_email,
                    kwargs={
                        "role": "contributor_application_to_maintainer",
                        "send_all": True,
                        "data": {
                            "name": "Maintainer(s)",
                            "project_name": project["project_name"],
                            "contributor_name": contributor["name"],
                            "contributor_email": contributor["email"],
                            "email": emails["email"],
                        },
                    },
                ).start()

                return JsonResponse(data={"admin_approved": True}, status=200)

            except ContributorErrors as e:
                return JsonResponse(data={"error": str(e)}, status=400)

    def get(self, request, **kwargs):

        Pagination = ["page"]
        SingleProject = ["projectId", "maintainer", "contributor"]
        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return project_pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_single_project(request, **kwargs)

        else:
            return JsonResponse(
                {"error": "Query Params are different from expected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def _remove_contributor(request, status) -> JsonResponse:
        """Send sns of contributor removal with blame

        Returns:
            JsonResponse
        """

        key = request.decoded

        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"Contributor -> {request.data.get('contributor_id')} removed by -> {key.get('user')}",
                    "subject": "[CONTRIBUTOR-REMOVE]",
                }
            },
        ).start()

        Thread(
            target=service.wrapper_email,
            kwargs={
                "role": "admin_contributor_rejection",
                "data": {
                    "name": status["name"],
                    "email": status["email"],
                    "project_name": status["project_name"],
                },
            },
        ).start()

        return JsonResponse(
            data={"removed": str(request.data.get("contributor_id"))}, status=200
        )

    @staticmethod
    def _remove_maintainer(request, status) -> JsonResponse:
        """Send sns of maintianer removal with blame

        Args:
            request

        Returns:
            JsonResponse
        """
        key = request.decoded
        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"Maintainer -> {request.data.get('maintainer_id')} removed by -> {key.get('user')}",
                    "subject": "[MAINTAINER-REMOVAL]",
                }
            },
        ).start()

        Thread(
            target=service.wrapper_email,
            kwargs={
                "role": "maintainer_application_rejection",
                "data": {
                    "name": status["name"],
                    "email": status["email"],
                    "project_name": status["project_name"],
                },
            },
        ).start()

        return JsonResponse(
            data={"removed": str(request.data.get("maintainer_id"))}, status=200
        )

    @staticmethod
    def _error_maintainer(request) -> JsonResponse:
        """Warning sns

        Args:
            request

        Returns:
            JsonResponse
        """
        key = request.decoded
        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"This admin messed up -> {key.get('user')} \
                trying to remove admin approved maintainer({request.data.get('maintainer_id')})",
                    "subject": "[WARNING-ADMIN-MESSED-UP]",
                }
            },
        ).start()

        return JsonResponse(data={"error": "Invalid request"}, status=400)

    @staticmethod
    def _error_contributor(request) -> JsonResponse:
        """Warning sns

        Args:
            request

        Returns:
            JsonResponse
        """
        key = request.decoded
        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"Tring to remove maintainer / admin or the contributor id is wrong\
                     approved contributor ({request.data.get('contributor_id')}), {key.get('user')} messed up.",
                    "subject": "[WARNING-ADMIN-MESSED-UP]",
                }
            },
        ).start()

        return JsonResponse(data={"error": "invalid request"}, status=400)

    def action_to_status(self, status: str, request) -> None:
        """Take action according to the response from remove functions

        Args:
            status (str): response
            request:  blame
        """
        if request.GET.get("role") == "contributor":
            if status:
                return self._remove_contributor(request=request, status=status)
            else:
                return self._error_contributor(request=request)
        else:
            if status:
                return self._remove_maintainer(request=request, status=status)
            else:
                return self._error_maintainer(request=request)

    def delete(self, request, **kwargs) -> JsonResponse:
        """Delete route for admin rejections

        Args:
            request

        Returns:
            JsonResponse
        """
        validate = RejectionSchema(
            data=request.data, params=request.GET.get("role")
        ).valid()
        if "error" in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        if request.GET.get("role") == "contributor":
            remove_status = entry.admin_remove_contributor(
                validate.get("contributor_id")
            )
            return self.action_to_status(status=remove_status, request=request)

        else:
            remove_status = entry.admin_remove_maintainer(validate.get("maintainer_id"))
            return self.action_to_status(status=remove_status, request=request)


class AdminAccepted(APIView):
    def get(self, request, **kwargs) -> JsonResponse:
        """pagination for all accepted projects

        Args:
            request

        Returns:
            JsonResponse
        """
        if "page" not in request.GET:
            return JsonResponse({"error": "Invalid query paramerts"}, status=400)

        return accepted_project_pagination(request=request)


class RefreshRoute(APIView):
    def post(self, request, **kwargs) -> JsonResponse:
        """Get new tokens from refresh token

        Args:
            request

        Returns:
            JsonResponse
        """
        refresh_token = get_token(request_header=request.headers)
        try:
            key = update_token(refresh_token=refresh_token)
            return JsonResponse(data=key, status=400)
        except AuthenticationErrors as e:
            return JsonResponse(data={"error": str(e)}, status=400)


class Verification(APIView):
    def get(self, request, **kwargs) -> JsonResponse:
        """Verify jwt

        Args:
            request

        Returns:
            JsonResponse
        """
        return JsonResponse(data={"success": True}, status=200)
