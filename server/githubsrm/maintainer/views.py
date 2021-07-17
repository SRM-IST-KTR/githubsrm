from hashlib import sha256

from administrator.issue_jwt import IssueKey
from apis import PostThrottle, check_token, service
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from threading import Thread
from maintainer import entry

from . import entry
from .definitions import MaintainerSchema
from .utils import project_pagination, project_single_project, RequestSetPassword

key = IssueKey()
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

            if entry.approve_contributor(validate.get("project_id"), validate.get("contributor_id")):
                return JsonResponse(data={
                    "approved contributor": True
                }, status=200)

            return JsonResponse(data={
                "error": "invalid ids or contributor already approved"
            }, status=400)

        return JsonResponse(data={
            "error": "Invalid reCaptcha token"
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
        user_credentials = entry.find_Maintainer_with_email(
            request.data["email"])

        if user_credentials["password"] != password_hashed:
            return JsonResponse(data={"message": "wrong password"}, status=status.HTTP_401_UNAUTHORIZED)

        doc_list = list(entry.find_all_Maintainer_with_email(
            request.data["email"]))

        payload = {}
        payload["email"] = doc_list[0]["email"]
        payload["name"] = doc_list[0]["name"]
        payload["project_id"] = [i["project_id"] for i in doc_list]

        if jwt := key.issue_key(payload):
            return JsonResponse(data={"key": jwt}, status=status.HTTP_200_OK)
        else:
            return JsonResponse(data={"message": "Does not exist"},  status=status.HTTP_401_UNAUTHORIZED)


class ResetPassword(APIView):

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Reset password

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
            if key.verify_key(key=jwt):
                Thread(target=entry.reset_password, kwargs={
                    "key": jwt,
                    "password": password
                }).start()

            return JsonResponse(data={}, status=200)

        return JsonResponse(data={
            "error": "Invalid recaptcha"
        }, status=401)


class SetPassword(APIView):

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
        doc = entry.find_Maintainer_with_email(email)

        # send 200 even if email is not found
        if not doc:
            return JsonResponse(status=status.HTTP_200_OK)

        jwt_link = RequestSetPassword(email)
        print(jwt_link)

        # TODO : ADD template here to send email
        # service.wrapper_email()

        # send 200 in all cases
        return JsonResponse(status=status.HTTP_200_OK)
