
from rest_framework import response, status
from rest_framework.views import APIView
from rest_framework import response, status


from .utils import project_SingleProject, project_Pagination


from .definitions import RegisterAdminSchema
from .perms import AdminPerms


class RegisterAdmin(APIView):
    permission_classes = [AdminPerms]

    def post(self, request, **kwargs):
        """Register Admins

        Args:
            request
        """
        valid = RegisterAdminSchema(request.data).valid()

        if 'error' in valid:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return response.Response(data=valid, status=status.HTTP_200_OK)


class ProjectsAdmin(APIView):

    def post(self, request, **kwargs):
        pass

    def get(self, request, **kwargs):

        Pagination = ['skip', 'limit', 'offset']

        SingleProject = ['projectId', 'maintainer', 'contributor']

        RequestQueryKeys = list(request.GET.keys())

        if len(set(Pagination) & set(RequestQueryKeys)) == 3:
            return project_Pagination(request, **kwargs)

        elif len(set(SingleProject) & set(RequestQueryKeys)) == 3:
            return project_SingleProject(request, **kwargs)

        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)