from .utils import check_token, BotoService
from rest_framework.views import APIView
from .definitions import *
from rest_framework import response, status
from .models import Entry
from .checks_models import EntryCheck
from bson import json_util
import json
import psutil
import time
import os
from django.shortcuts import render

entry = Entry()
entry_checks = EntryCheck()
service = BotoService()


def home(request):
    return render(request, 'index.html')


class Contributor(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_scope = 'common'

    def post(self, request, **kwargs) -> response.Response:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            response.Response
        """
        if check_token(request.META.get('HTTP_X_RECAPTCHA_TOKEN')):
            validate = CommonSchema(
                request.data, query_param=request.GET.get('role')).valid()

            if 'error' not in validate:
                if entry_checks.check_contributor(validate['interested_project'],
                                                  validate['reg_number']):
                    return response.Response({
                        "invalid data": "Contributor for project exists / Project not approved"
                    }, status=status.HTTP_400_BAD_REQUEST)

                if entry.enter_contributor(validate):
                    if service.wrapper_email(role='contributor', data=validate):
                        return response.Response({
                            "valid": validate
                        }, status=status.HTTP_201_CREATED)
                    return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return response.Response({
                    "error": "project not approved or project does not exist"
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

        result = json.loads(json_util.dumps(entry.get_contributors()))
        return response.Response({
            "contributors": result
        }, status=status.HTTP_200_OK)


class Maintainer(APIView):
    '''
    Maintainer API to Allow addition of maintainers to the database 
    '''
    throttle_scope = 'common'

    def post(self, request, **kwargs) -> response.Response:
        """Accept Maintainers

        Args:
            request 

        Returns:
            Response
        """
        if check_token(request.META.get('HTTP_X_RECAPTCHA_TOKEN')):

            validate = CommonSchema(
                request.data, query_param=request.GET.get('role')).valid()

            if 'error' not in validate:

                if 'project_id' in validate:
                    # BETA MAINTAINER
                    if entry_checks.validate_beta_maintainer(doc=validate):
                        if id := entry.enter_beta_maintainer(doc=request.data):

                            if service.wrapper_email(role='beta', data=validate):
                                return response.Response(status=status.HTTP_201_CREATED)
                            else:
                                entry.delete_beta_maintainer(maintainer_id=id,
                                                             project_id=validate.get('project_id'))

                            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return response.Response(data={
                        "error": "Approved / Already Exists / Invalid"
                    }, status=status.HTTP_409_CONFLICT)

                if entry_checks.check_existing(description=validate['description'],
                                               project_name=validate['project_name']):
                    # Enter alpha maintainer

                    return response.Response({
                        "error": "Project Exists"
                    }, status=status.HTTP_409_CONFLICT)

                if value := entry.enter_maintainer(validate):
                    validate['project_id'] = value[0]
                    validate['project_name'] = value[2]
                    if service.wrapper_email(role='alpha', data=validate):
                        return response.Response(status=status.HTTP_201_CREATED)
                    else:
                        entry.delete_alpha_maintainer(
                            project_id=validate.get('project_id'),
                            maintainer_id=value[1])
                    return response.Response({
                        "deleted record"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return response.Response(validate.get('error'), status=status.HTTP_400_BAD_REQUEST)

        return response.Response({
            "error": "Invalid reCaptcha"
        }, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, **kwargs) -> response.Response:
        """Get all projects

        Args:
            request ([type])
        """

        result = json.loads(json_util.dumps(entry.get_projects()))

        return response.Response(data=result, status=status.HTTP_200_OK)


class Team(APIView):
    """
    Team data route

    Args:
        APIView
    """
    throttle_scope = 'common'

    def get(self, request, **kwargs) -> response.Response:
        """
        Get Full team data

        Args:
            request
        """

        result = json.loads(json_util.dumps(entry.get_team_data()))
        return response.Response(result, status=status.HTTP_200_OK)


class ContactUs(APIView):
    """
    ContactUs route

    Args:
        APIView 
    """

    def post(self, request, **kwargs) -> response.Response:
        """Handles post data

        Args:
            request

        Returns:
            response.Response
        """
        if check_token(request.META.get('HTTP_X_RECAPTCHA_TOKEN')):
            validate = ContactUsSchema(data=request.data).valid()
            if 'error' in validate:
                return response.Response(data={
                    "error": validate.get('error')
                }, status=status.HTTP_400_BAD_REQUEST)

            result = entry.enter_contact_us(doc=request.data)
            if result:
                service.sns(
                    message=f'New Query Received! \n Name:{validate.get("name")} \n \
                        Email: {validate.get("email")} \n \
                        Message: {validate.get("message")} \n \
                        Phone Number: {validate.get("phone_number")}')

                return response.Response(status=status.HTTP_201_CREATED)
            return response.Response(data={
                "entry exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(data={
            "invalid reCaptcha"
        }, status=status.HTTP_400_BAD_REQUEST)


class HealthCheck(APIView):
    """Health Checker route

    Args:
        APIView 
    """

    throttle_scope = 'common'

    def get(self, request, **kwargs) -> response.Response:
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
