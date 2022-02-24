from threading import Thread

from core.aws import service
from core.settings import PostThrottle
from core.utils import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from administrator import entry, jwt_keys

from .definitions import AdminSchema, ApprovalSchema, RejectionSchema
from .perms import AuthAdminPerms
from .utils import (
    accepted_project_pagination,
    alpha_maintainer_support,
    beta_maintainer_support,
    get_token,
    project_pagination,
    project_single_project,
    update_token,
)


class ProjectsAdmin(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        try:
            params = request.GET["role"]
        except Exception:
            return JsonResponse(data={"error": "invalid query parameters"}, status=400)

        validate = ApprovalSchema(request.data, params=params).valid()
        if params == "maintainer":
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
        elif params == "project":
            project = entry.approve_project(
                identifier=validate.get("project_id"), year=validate.get("year")
            )
            email_document = entry.get_all_maintainer_emails(project=project)
            if email_document:
                email_status = service.wrapper_email(
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
                )
                if not email_status:
                    entry.reset_status_project(project=project)
                    return JsonResponse(data={}, status=500)

                return JsonResponse(
                    data={"Approved Project": validate.get("project_id")},
                    status=200,
                )
            else:
                entry.reset_status_project(project=project)
                blame = request.decoded.get("user")
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

        else:
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

    def get(self, request, **kwargs):
        pagination = ["page"]
        single_project = ["projectId", "maintainer", "contributor"]
        request_query_keys = list(request.GET.keys())

        if len(set(pagination) & set(request_query_keys)) == 1:
            return project_pagination(request, **kwargs)

        elif len(set(single_project) & set(request_query_keys)) == 3:
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

    def delete(self, request) -> JsonResponse:
        validate = RejectionSchema(
            data=request.data, params=request.GET.get("role")
        ).valid()

        if request.GET.get("role") == "contributor":
            remove_status = entry.admin_remove_contributor(
                validate.get("contributor_id")
            )
            return self.action_to_status(status=remove_status, request=request)

        else:
            remove_status = entry.admin_remove_maintainer(validate.get("maintainer_id"))
            return self.action_to_status(status=remove_status, request=request)


@api_view(["POST"], permission_classes=[AuthAdminPerms])
def register_admin(request) -> JsonResponse:
    entry.insert_admin(request.data)
    return JsonResponse(data={"registred": True}, status=200)


@api_view(["POST"])
def admin_login(request) -> JsonResponse:
    validate = AdminSchema(request.data).valid()
    password = validate.get("password")

    entry.verify_admin(email=validate.get("email"), password=password)
    keys = jwt_keys.issue_key(
        payload={"admin": True, "user": validate.get("email")},
        get_refresh_token=True,
    )
    return JsonResponse(data=keys, status=200)


@api_view(["GET"])
def admin_accepted(request) -> JsonResponse:
    if "page" not in request.GET:
        return JsonResponse({"error": "Invalid query paramerts"}, status=400)

    return accepted_project_pagination(request=request)


@api_view(["POST"])
def refresh(request) -> JsonResponse:
    refresh_token = get_token(request_header=request.headers)
    key = update_token(refresh_token=refresh_token)
    return JsonResponse(data=key, status=400)


@api_view(["GET"])
def verify(request) -> JsonResponse:
    return JsonResponse(data={"success": True}, status=200)
