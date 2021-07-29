import json
import os
import time
from threading import Thread

import psutil
from bson import json_util
from django.http import JsonResponse
from rest_framework.views import APIView

from apis import (PostThrottle, open_entry, open_entry_checks,
                  service)

from .definitions import *
from django.shortcuts import redirect


def catch_all(request, path=None):
    return redirect("https://githubsrm.tech")


class Contributor(APIView):
    '''
    Contributors API Allows additon of contributors to the database
    '''
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            JsonResponse
        """
        validate = CommonSchema(
            request.data, query_param=request.GET.get('role')).valid()

        if 'error' in validate:
            return JsonResponse(data={
                "error": "Invalid data"
            }, status=400)

        if open_entry_checks.check_contributor(validate['interested_project'],
                                               validate['reg_number'], validate["github_id"],
                                               validate["srm_email"]):
            return JsonResponse(data={
                "invalid data": "Contributor for project exists / Project not approved"
            }, status=400)

        if doc := open_entry.enter_contributor(validate):
            if service.wrapper_email(role='contributor_received', data={"contribution": validate["poa"],
                                                                        "project_name": doc["project_name"], "name": doc["name"], "email": doc["email"]}):

                Thread(target=service.sns, kwargs={
                    "payload": {
                        "message": f"A new contributor has applied for this project -> {doc.get('interested_project')}",
                        "subject": "[CONTRIBUTOR-ENTRY] New Contributor Applied"
                    }
                }).start()

                return JsonResponse(data={}, status=201)
            else:
                return JsonResponse(data={}, status=500)
        else:
            return JsonResponse(data={
                "error": "project not approved or project does not exist"
            }, status=400)


class Maintainer(APIView):
    '''
    Maintainer API to Allow addition of maintainers to the database
    '''
    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Accept Maintainers

        Args:
            request

        Returns:
            Response
        """
        validate = CommonSchema(
            request.data, query_param=request.GET.get('role')).valid()
        if 'error' in validate:
            return JsonResponse(data={
                "error": validate.get('error')
            }, status=400)

        if 'project_id' in validate:
            if details := open_entry_checks.validate_beta_maintainer(doc=validate):

                if id := open_entry.enter_beta_maintainer(doc=request.data):

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
                        return JsonResponse(data={}, status=201)
                    else:
                        open_entry.beta_maintainer_reset_status(
                            maintainer_id=id)

                    return JsonResponse(data={}, status=500)

            return JsonResponse(data={
                "error": "Approved / Already Exists / Invalid"
            }, status=400)

        elif open_entry_checks.check_existing(description=validate['description'],
                                              project_name=validate['project_name'],
                                              project_url=validate['project_url']):

            return JsonResponse(data={
                "error": "Project Exists"
            }, status=409)

        elif value := open_entry.enter_maintainer(validate):
            validate['project_id'] = value[0]
            validate['project_name'] = value[2]
            validate['description'] = value[3]

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
                return JsonResponse(data={}, status=201)
            else:
                open_entry.alpha_maintainer_reset_status(
                    project_id=validate.get('project_id'),
                    maintainer_id=value[1])
            return JsonResponse({
                "deleted record"
            }, status=500)

    def get(self, request, **kwargs) -> JsonResponse:
        """Get all projects

        Args:
            request
        """

        result = json.loads(json_util.dumps(open_entry.get_projects()))

        return JsonResponse(data=result, status=200, safe=False)


class Team(APIView):
    """
    Team data route

    Args:
        APIView
    """
    throttle_classes = [PostThrottle]

    def get(self, request, **kwargs) -> JsonResponse:
        """
        Get Full team data

        Args:
            request
        """

        result = json.loads(json_util.dumps(open_entry.get_team_data()))
        return JsonResponse(result, status=200, safe=False)


class ContactUs(APIView):
    """
    ContactUs route

    Args:
        APIView
    """

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Handles post data

        Args:
            request

        Returns:
            JsonResponse
        """

        validate = ContactUsSchema(data=request.data).valid()
        if 'error' in validate:
            return JsonResponse(data={
                "error": validate.get('error')
            }, status=400)

        result = open_entry.enter_contact_us(doc=request.data)
        if result:
            Thread(target=service.sns, kwargs={'payload': {
                'message': f'New Query Received! \n Name:{validate.get("name")} \n \
                    Email: {validate.get("email")} \n \
                    Message: {validate.get("message")} \n \
                    Phone Number: {validate.get("phone_number")}',
                'subject': '[QUERY]: https://githubsrm.tech'
            }}).start()

            return JsonResponse(data={}, status=201)
        return JsonResponse(data={
            "error": "entry exists"
        }, status=400)


class HealthCheck(APIView):
    """Health Checker route

    Args:
        APIView
    """

    throttle_classes = [PostThrottle]

    def get(self, request, **kwargs) -> JsonResponse:
        """Get Process UpTime

        Args:
            request
        """

        uptime = time.time() - psutil.Process(os.getpid()).create_time()
        return JsonResponse({
            "uptime": uptime,
            "status": "OK",
            "timeStamp": time.time()
        }, status=200)
