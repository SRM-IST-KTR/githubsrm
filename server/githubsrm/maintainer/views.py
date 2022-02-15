from threading import Thread

from administrator import jwt_keys
from administrator.utils import get_token
from core.aws import service
from core.settings import PostThrottle
from django.http.response import JsonResponse
from rest_framework.views import APIView

from maintainer import entry

from .definitions import MaintainerSchema, RejectionSchema
from .utils import RequestSetPassword, project_pagination, project_single_project


class Projects(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        validate = MaintainerSchema(
            request.data, path=request.path.split("maintainer/")[1]
        ).valid()

        doc = entry.approve_contributor(
            validate.get("project_id"), validate.get("contributor_id")
        )
        service.wrapper_email(
            role="contributor_approval",
            data={
                "email": doc["email"],
                "name": doc["name"],
                "project_name": doc["project_name"],
                "project_url": doc["project_url"],
            },
        )
        return JsonResponse(data={"success": True}, status=200)

    @staticmethod
    def _remove_contributor(request) -> JsonResponse:
        contributor = entry.find_contributor_for_removal(
            request.data.get("contributor_id"), request.decoded.get("project_id")
        )
        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"Maintainer removed contributor ({request.data.get('contributor_id')}) \
                    removed by -> {request.decoded.get('email')}",
                    "status": "[MAINTAINER-REMOVED-CONTRIBUTOR]",
                }
            },
        ).start()
        Thread(
            target=service.wrapper_email,
            kwargs={
                "role": "maitainer_contributor_rejection",
                "data": {
                    "name": contributor["name"],
                    "email": contributor["email"],
                    "project_name": contributor["project_name"],
                },
            },
        ).start()

        return JsonResponse(
            data={"removed": request.data.get("contributor_id")}, status=200
        )

    def delete(self, request) -> JsonResponse:
        RejectionSchema(data=request.data).valid()
        _, token = get_token(request_header=request.headers)
        decoded = jwt_keys.verify_key(token)
        if decoded:
            request.decoded = decoded
        else:
            return JsonResponse(data={"error": "Invalid key"}, status=401)
        return self._remove_contributor(request=request)

    def get(self, request) -> JsonResponse:
        pagination = ["page"]
        single_project = ["projectId", "maintainer", "contributor"]

        request_query_keys = list(request.GET.keys())
        if len(set(pagination) & set(request_query_keys)) == 1:
            response = project_pagination(request)
            if "error" in response:
                return JsonResponse(response, status=401)
            else:
                return JsonResponse(response, status=200)

        elif len(set(single_project) & set(request_query_keys)) == 3:
            return JsonResponse(
                project_single_project(request),
                status=200,
                safe=False,
            )

        else:
            return JsonResponse(
                data={"error": "invalid query parameters"},
                status=400,
            )


class Login(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        MaintainerSchema(
            request.data, path=request.path.split("maintainer/")[1]
        ).valid()
        user_credentials = entry.find_Maintainer_credentials_with_email(
            request.data["email"]
        )

        if not user_credentials:
            return JsonResponse(
                data={"error": "Maintainer not found / Not approved"}, status=400
            )

        entry.check_hash(request.data["email"], request.data["password"])
        doc_list = list(entry.find_all_Maintainer_with_email(request.data["email"]))

        if doc_list:
            payload = {}
            payload["email"] = doc_list[0]["email"]
            payload["name"] = doc_list[0]["name"]
            payload["project_id"] = [i["project_id"] for i in doc_list]

            jwt = jwt_keys.issue_key(payload, get_refresh_token=True)
            return JsonResponse(data=jwt, status=200)

        return JsonResponse(data={"error": "Email not found"}, status=400)


class SetPassword(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        MaintainerSchema(
            request.data, path=request.path.split("maintainer/")[1]
        ).valid()

        try:
            token = request.headers.get("Authorization").split()
            token_type, token = token[0], token[1]
            assert token_type == "Bearer"
        except (ValueError, AssertionError):
            return JsonResponse(data={"error": "Invalid token"}, status=400)

        password = request.data.get("password")
        jwt_keys.verify_key(key=token)
        entry.set_password(key=token, password=password)
        return JsonResponse(data={}, status=200)


class ResetPassword(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        MaintainerSchema(
            request.data, path=request.path.split("maintainer/")[1]
        ).valid()

        email = request.data.get("email")
        doc = entry.find_Maintainer_credentials_with_email(email)
        # send 200 even if email is not found
        if not doc:
            return JsonResponse({}, status=200)

        maintainer = entry.find_Maintainer_with_email(email)

        jwt_link = RequestSetPassword(email)
        service.wrapper_email(
            role="forgot_password",
            data={"name": maintainer["name"], "email": email, "reset_token": jwt_link},
        )

        # send 200 in all cases
        return JsonResponse({}, status=200)
