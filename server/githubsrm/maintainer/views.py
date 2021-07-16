from hashlib import sha256
from xml.dom.minidom import Entity

from administrator.issue_jwt import IssueKey
from apis import PostThrottle, check_token
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from maintainer import entry

from . import entry
from .definitions import MaintainerSchema
from .utils import project_pagination, project_single_project

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
            return JsonResponse(project_single_project(request, **kwargs), status=status.HTTP_200_OK)

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
        user_credentials = entry.find_Maintainer_with_email(request.data["email"])

        if user_credentials["password"] != password_hashed:
            return JsonResponse(data={"message": "wrong password"}, status=status.HTTP_401_UNAUTHORIZED)

        doc_list = list(entry.find_all_Maintainer_with_email(request.data["email"]))

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
        """Handle reset password

        Args:
            request

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

            validate = MaintainerSchema(request.data, request.path).valid()
            if 'error' in validate:
                return JsonResponse(data={
                    "error": str(validate.get("error"))
                }, status=400)

            if entry.update_password(email=request.data.get("email")):
                return JsonResponse(data={
                    "updated password": True
                }, status=200)

            return JsonResponse(data={
                "error": "invalid credentials"
            }, status=400)

        return JsonResponse(data={
            "error": "Invalid reCaptcha token"
        }, status=401)
