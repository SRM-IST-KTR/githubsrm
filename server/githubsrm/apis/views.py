from rest_framework.views import APIView
from .definations import *
from rest_framework import response, status
from .models import Entry
from bson import json_util
import json


class Contribute(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_scope = 'common'
    entry = Entry()

    def post(self, request, **kwargs) -> response.Response:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            response.Response
        """
        validate = CommonSchema(request.data, headers={
            "path_info": request.path_info
        }).valid()

        if 'error' not in validate:
            if self.entry.check_existing_contributor(validate['interested_project'], validate['reg_number']):
                return response.Response({
                    "invalid data": "Contributor For project exists"
                }, status=status.HTTP_400_BAD_REQUEST)

            if self.entry.enter_contributor(validate):
                return response.Response({
                    "valid": validate
                }, status=status.HTTP_201_CREATED)

            return response.Response({
                "invalid project": validate['interested_project']
            }, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(validate.get('error'), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs) -> response.Response:
        """Return all Contributors

        Args:
            request

        Returns:
            response.Response
        """

        result = json.loads(json_util.dumps(self.entry.get_contributors()))
        return response.Response({
            "contributors": result
        }, status=status.HTTP_200_OK)


class Maintainer(APIView):
    '''
    Maintainer API to Allow addition of maintainers to the database 
    '''
    throttle_scope = 'common'
    entry = Entry()

    def post(self, request, **kwargs) -> response.Response:
        """Accept Maintainers

        Args:
            request 

        Returns:
            Response
        """

        validate = CommonSchema(request.data, headers={
            "path_info": request.path_info
        }).valid()
        if 'error' not in validate:
            if self.entry.check_existing(validate['poa']):
                return response.Response({
                    "invalid": "Project exists"
                }, status=status.HTTP_400_BAD_REQUEST)

            if self.entry.enter_maintainer(validate):
                return response.Response(validate, status=status.HTTP_200_OK)
        return response.Response(validate.get('error'), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs) -> response.Response:
        """Get all projects

        Args:
            request ([type])
        """
        result = json.loads(json_util.dumps(self.entry.get_projects()))

        return response.Response({
            "projects": result
        }, status=status.HTTP_200_OK)
