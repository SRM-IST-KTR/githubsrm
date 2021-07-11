from hashlib import sha256

from administrator.issue_jwt import IssueKey
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from maintainer import entry

from . import entry
from .definitions import MaintainerSchema
from .utils import Projects_pagnation, project_SingleProject

key = IssueKey()
db = entry.db


class Projects(APIView):

    def post(self, request, **kwargs) -> JsonResponse:
        """Accept contributors. 

        Args:
            request

        Returns:
            JsonResponse
        """

        validate = MaintainerSchema(request.data, path=request.path).valid()

        if 'error' in validate:
            return JsonResponse(data=validate, status=400)

        if entry.approve_contributor(validate.get("project_id"), validate.get("contributor_id")):
            return JsonResponse(data={
                "approved contributor": True
            }, status=200)

        return JsonResponse(data={
            "error": "invalid ids or contributor already approved"
        }, status=400)

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
            return JsonResponse(Projects_pagnation(request, **kwargs), status=status.HTTP_200_OK)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return JsonResponse(project_SingleProject(request, **kwargs), status=status.HTTP_200_OK)

        else:
            return JsonResponse(data={
                "error": "invalid query parameters"
            }, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request, **kwargs) -> JsonResponse:
        """
        Login route get email and password make jwt and send.
        """

        validate = MaintainerSchema(request.data, path=request.path).valid()
        if 'error' in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        password_hashed = sha256(request.data["password"].encode()).hexdigest()
        doc_list_iter = entry.Send_all_Maintainer_email(request.data["email"])
        doc_list = [i for i in doc_list_iter]

        if len(doc_list):
            if doc_list[0]["password"] != password_hashed:
                return JsonResponse({"message": "wrong password"},
                                    status=status.HTTP_401_UNAUTHORIZED)

            payload = {}
            payload["email"] = doc_list[0]["email"]
            payload["name"] = doc_list[0]["name"]
            payload["project_id"] = [i["project_id"] for i in doc_list]

            if jwt := key.issue_key(payload):
                return JsonResponse({"key": jwt}, status=status.HTTP_200_OK)

        return JsonResponse({"message": "Does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
