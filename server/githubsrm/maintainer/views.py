from django.http.response import JsonResponse
from .utils import project_SingleProject, Projects_pagnation
from .definitions import MaintainerSchema
from rest_framework import status
from rest_framework.views import APIView
from maintainer import entry


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
