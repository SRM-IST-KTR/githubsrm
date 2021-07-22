from hashlib import sha256
from threading import Thread

from apis import PostThrottle, check_token, service
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from maintainer import entry
from administrator import jwt_keys
from administrator.utils import get_token
from . import entry
from .definitions import MaintainerSchema
from .utils import (
    RequestSetPassword, project_pagination,
    project_single_project
)


db = entry.db


class Projects(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Accept contributors.

        Args:
            request

        Returns:
            JsonResponse
        """

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return JsonResponse(data={
                "error": "recaptcha not provided"
            }, status=401)

        if check_token(reCaptcha):

            validate = MaintainerSchema(
                request.data, path=request.path).valid()

            if 'error' in validate:
                return JsonResponse(data=validate, status=400)

            if doc := entry.approve_contributor(validate.get("project_id"), validate.get("contributor_id")):
                service.wrapper_email(role="contributor_approval", data={
                    "email": doc["email"],
                    "name": doc["name"],
                    "project_name": doc["project_name"],
                    "project_url": doc["project_url"]
                })

                return JsonResponse(data={
                    "approved contributor": True
                }, status=200)

            return JsonResponse(data={
                "error": "invalid ids or contributor already approved"
            }, status=400)

        return JsonResponse(data={
            "error": "Invalid reCaptcha token"
        }, status=401)

    @staticmethod
    def _remove_contributor(request) -> JsonResponse:
        """Send sns for contributor removal

        Args:
            request

        Returns:
            JsonResponse
        """
        key = jwt_keys.verify_key(get_token(request.META))
        contributor = entry.find_contributor_for_removal(
            request.data.get("contributor_id"))
        if contributor:

            if contributor["interested_project"] in key.get("project_id"):

                entry.remove_contributor(
                    identifier=contributor["_id"])

                Thread(target=service.sns, kwargs={
                    "payload": {
                        "message": f"Maintainer removed contributor ({request.data.get('contributor_id')}) \
                            removed by -> {key.get('email')}",
                        "status": "[MAINTAINER-REMOVED-CONTRIBUTOR]"
                    }
                }).start()

                return JsonResponse(data={
                    "removed": request.data.get("contributor_id")
                }, status=200)

            else:
                return JsonResponse(data={
                    "error": "Invalid request"
                }, status=400)
        else:
            return JsonResponse(data={
                "error": "invalid request"
            }, status=400)

    def delete(self, request, **kwargs) -> JsonResponse:
        """Remove contributors

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
            return self._remove_contributor(request=request)
        else:
            return JsonResponse(data={
                "error": "Invaid token"
            }, status=401)

    def get(self, request, **kwargs) -> JsonResponse:
        """Projects get view for maintainer portal.

        Args:
            request

        Returns:
            JsonResponse
        """
        Pagination = ['page']
        SingleProject = ['projectId', 'maintainer', 'contributor']

        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 1:
            return JsonResponse(project_pagination(request, **kwargs), status=status.HTTP_200_OK)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return JsonResponse(project_single_project(request, **kwargs), status=status.HTTP_200_OK, safe=False)

        else:
            return JsonResponse(data={
                "error": "invalid query parameters"
            }, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """
        Login route get email and password make jwt and send.
        """

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return JsonResponse(data={"error": "recaptcha not provided"}, status=401)

        if not check_token(reCaptcha):
            return JsonResponse(data={"error": "Invalid recaptcha token"}, status=401)

        validate = MaintainerSchema(request.data, path=request.path).valid()
        if 'error' in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        password_hashed = sha256(request.data["password"].encode()).hexdigest()
        user_credentials = entry.find_Maintainer_credentials_with_email(
            request.data["email"])

        if not user_credentials:
            return JsonResponse(data={
                "error": "Maintainer not found / Not approved"
            }, status=400)

        if user_credentials["password"] != password_hashed:
            return JsonResponse(data={"message": "wrong password"}, status=status.HTTP_401_UNAUTHORIZED)

        doc_list = list(entry.find_all_Maintainer_with_email(
            request.data["email"]))

        if doc_list:

            payload = {}
            payload["email"] = doc_list[0]["email"]
            payload["name"] = doc_list[0]["name"]
            payload["project_id"] = [i["project_id"] for i in doc_list]

            if jwt := key.issue_key(payload):
                return JsonResponse(data={"key": jwt}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(data={"message": "Does not exist"},  status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse(data={
            "error": "Email not found"
        }, status=400)


class SetPassword(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """set password

        Args:
            request

        Returns:
            JsonResponse
        """
        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return JsonResponse(data={"error": "recaptcha not provided"}, status=401)

        if check_token(reCaptcha):
            validate = MaintainerSchema(
                data=request.data, path=request.path).valid()
            if 'error' in validate:
                return JsonResponse(data={"error": validate.get("error")}, status=400)

            try:
                token = request.headers.get("Authorization").split()
                token_type, token = token[0], token[1]
                assert token_type == 'Bearer'
            except Exception as e:
                return JsonResponse(data={
                    "error": "Invalid token"
                }, status=400)

            jwt = token

            password = request.data.get("password")

            if not jwt_keys.verify_key(key=jwt):
                return JsonResponse(data={"error": "Invalid jwt"}, status=400)

            if not entry.set_password(key=jwt, password=password):
                return JsonResponse(data={"error": "Already changed"}, status=400)

            return JsonResponse(data={}, status=200)

        return JsonResponse(data={
            "error": "Invalid recaptcha"
        }, status=401)


class ResetPassword(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            print(e)
            return JsonResponse(data={"error": "recaptcha not provided"}, status=401)

        if not check_token(reCaptcha):
            return JsonResponse(data={"error": "Invalid recaptcha"}, status=401)

        validate = MaintainerSchema(
            data=request.data, path=request.path).valid()
        if 'error' in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        email = request.data.get("email")
        doc = entry.find_Maintainer_credentials_with_email(email)
        # send 200 even if email is not found
        if not doc:
            return JsonResponse({}, status=status.HTTP_200_OK)

        maintainer = entry.find_Maintainer_with_email(email)

        jwt_link = RequestSetPassword(email)
        print(jwt_link)

        service.wrapper_email(role="forgot_password", data={
                              "name": maintainer["name"], "email": email, "reset_token": jwt_link})

        # send 200 in all cases
        return JsonResponse({}, status=status.HTTP_200_OK)
