import json
import os
import time
from threading import Thread

import psutil
from bson import json_util
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from rest_framework import response, status
from rest_framework.views import APIView

from apis import (PostThrottle, check_token, open_entry, open_entry_checks,
                  service)

from .definitions import *
from .utils import conditional_render


def home(request, path=None):
    try:
        return render(request, f'{conditional_render(path)}')
    except TemplateDoesNotExist as e:
        return render(request, '404.html')


class Contributor(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> response.Response:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            response.Response
        """

        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return response.Response({
                "error": "reCaptcha token not provided"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if check_token(reCaptcha):

            try:
                validate = CommonSchema(
                    request.data, query_param=request.GET.get('role')).valid()
            except Exception as e:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

            if 'error' not in validate:
                if open_entry_checks.check_contributor(validate['interested_project'],
                                                       validate['reg_number'], validate["github_id"],
                                                       validate["srm_email"]):
                    return response.Response({
                        "invalid data": "Contributor for project exists / Project not approved"
                    }, status=status.HTTP_400_BAD_REQUEST)

                if doc := open_entry.enter_contributor(validate):
                    if service.wrapper_email(role='contributor_received', data={"contribution": validate["poa"],
                                                                                "project_name": doc["project_name"], "name": doc["name"], "email": doc["email"]}):
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

        result = json.loads(json_util.dumps(open_entry.get_contributors()))
        return response.Response({
            "contributors": result
        }, status=status.HTTP_200_OK)


class Maintainer(APIView):
    '''
    Maintainer API to Allow addition of maintainers to the database
    '''
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> response.Response:
        """Accept Maintainers

        Args:
            request

        Returns:
            Response
        """
        try:
            reCaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
        except KeyError as e:
            return response.Response({
                "error": "reCaptcha token not provided"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if check_token(reCaptcha):

            try:
                validate = CommonSchema(
                    request.data, query_param=request.GET.get('role')).valid()
            except Exception as e:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

            if 'error' not in validate:

                if 'project_id' in validate:

                    if details := open_entry_checks.validate_beta_maintainer(doc=validate):

                        if id := open_entry.enter_beta_maintainer(doc=request.data):
                            # TODO ROLL BACK
                            if service.wrapper_email(role='maintainer_received', data={
                                "name": validate["name"],
                                "project_name": details["project_name"],
                                "email": validate["email"]
                            }):
                                Thread(target=service.sns, kwargs={'payload': {
                                    'message': f'New Beta Maintainer for Project ID {validate.get("project_id")}\n \
                                        Details: \n \
                                        Name: {validate.get("name")} \n \
                                        Email Personal: {validate.get("email")}',
                                    'subject': '[BETA-MAINTAINER]: https://githubsrm.tech'
                                }}).start()
                                return response.Response(status=status.HTTP_201_CREATED)
                            else:
                                open_entry.delete_beta_maintainer(maintainer_id=id,
                                                                  project_id=validate.get('project_id'))

                            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return response.Response(data={
                        "error": "Approved / Already Exists / Invalid"
                    }, status=status.HTTP_400_BAD_REQUEST)

                if open_entry_checks.check_existing(description=validate['description'],
                                                    project_name=validate['project_name'],
                                                    project_url=validate['project_url']):

                    return response.Response({
                        "error": "Project Exists"
                    }, status=status.HTTP_409_CONFLICT)

                if value := open_entry.enter_maintainer(validate):
                    validate['project_id'] = value[0]
                    validate['project_name'] = value[2]
                    validate['description'] = value[3]
                    # TODO ROLL BACK HERE IF FAILS
                    if service.wrapper_email(role='project_submission_confirmation', data={
                        "project_name": validate["project_name"],
                        "name": validate["name"],
                        "project_description": validate["description"],
                        "email": validate["email"]

                    }):
                        Thread(target=service.sns, kwargs={'payload': {
                            'message': f'New Alpha Maintainer for Project ID {validate.get("project_id")}\n \
                                        Details: \n \
                                        Name: {validate.get("name")} \n \
                                        Email Personal: {validate.get("email")} \n \
                                        Project Details: \n \
                                        Name: {validate.get("project_name")} \n \
                                        Description: {validate.get("description")}',
                            'subject': '[ALPHA-MAINTAINER]: https://githubsrm.tech'
                        }}).start()
                        return response.Response(status=status.HTTP_201_CREATED)
                    else:
                        open_entry.delete_alpha_maintainer(
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

        result = json.loads(json_util.dumps(open_entry.get_projects()))

        return response.Response(data=result, status=status.HTTP_200_OK)


class Team(APIView):
    """
    Team data route

    Args:
        APIView
    """
    throttle_classes = [PostThrottle]

    def get(self, request, **kwargs) -> response.Response:
        """
        Get Full team data

        Args:
            request
        """

        result = json.loads(json_util.dumps(open_entry.get_team_data()))
        return response.Response(result, status=status.HTTP_200_OK)


class ContactUs(APIView):
    """
    ContactUs route

    Args:
        APIView
    """

    throttle_classes = [PostThrottle]

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

            result = open_entry.enter_contact_us(doc=request.data)
            if result:
                Thread(target=service.sns, kwargs={'payload': {
                    'message': f'New Query Received! \n Name:{validate.get("name")} \n \
                        Email: {validate.get("email")} \n \
                        Message: {validate.get("message")} \n \
                        Phone Number: {validate.get("phone_number")}',
                    'subject': '[QUERY]: https://githubsrm.tech'
                }}).start()

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

    throttle_classes = [PostThrottle]

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
