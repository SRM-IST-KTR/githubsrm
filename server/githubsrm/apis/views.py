from .utils import checkToken
from rest_framework.views import APIView
from .definitions import *
from rest_framework import response, status
from .models import Entry
from bson import json_util
import json
import psutil
import time
import os


class Contributor(APIView):
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
        if checkToken(request.META.get('HTTP_X_RECAPTCHA_TOKEN')):
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
        return response.Response({
            "error": "Invalid reCaptcha"
        }, status=status.HTTP_401_UNAUTHORIZED)

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
        if checkToken(request.META.get('HTTP_X_RECAPTCHA_TOKEN')):
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
        return response.Response({
            "error": "Invalid reCaptcha"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, **kwargs) -> response.Response:
        """Get all projects

        Args:
            request ([type])
        """
        result = json.loads(json_util.dumps(self.entry.get_projects()))

        return response.Response({
            "projects": result
        }, status=status.HTTP_200_OK)


class HealthCheck(APIView):
    """Health Checker route

    Args:
        APIView 
    """

    throttle_scope = 'common'

    def get(self, request, **kwargs):
        """Get Process UpTime

        Args:
            request 
        """
        
        uptime = time.time() - psutil.Process(os.getpid()).create_time()
        return response.Response({
            "uptime": uptime,
            "status": "OK",
            "timeStamp": time.time()
        }, status=status.HTTP_200_OK)

class Team(APIView):
    """
    Team data route

    Args:
        APIView
    """
    throttle_scope = 'common'
    entry = Entry()

    def get(self, request, **kwargs):
        """
        Get Full team data

        Args:
            request
        """
        result = self.entry.get_team_data()
        return response.Response({
            "team_data": result
        }, status=status.HTTP_200_OK)


