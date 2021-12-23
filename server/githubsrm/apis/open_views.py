import json
import os
import time
from threading import Thread

import psutil
from bson import json_util
from core import service
from core.settings import PostThrottle
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from apis import open_entry, open_entry_checks

from .definitions import *


def catch_all(request, path=None):
    return redirect("https://githubsrm.tech")


class Contributor(APIView):
    """
    Contributors API Allows additon of contributors to the database
    """

    throttle_classes = [PostThrottle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Adding Contributors to Projects

        Args:
            request

        Returns:
            JsonResponse
        """
        validate = CommonSchema(
            request.data, query_param=request.GET.get("role")
        ).valid()

        if "error" in validate:
            return JsonResponse(data={"error": "Invalid data"}, status=400)

        open_entry_checks.check_contributor(
            validate["interested_project"],
            validate["reg_number"],
            validate["github_id"],
            validate["srm_email"],
        )

        doc = open_entry.enter_contributor(validate)
        email_status = service.wrapper_email(
            role="contributor_received",
            data={
                "contribution": validate["poa"],
                "project_name": doc["project_name"],
                "name": doc["name"],
                "email": doc["email"],
            },
        )
        if not email_status:
            return JsonResponse(data={}, status=500)

        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f"A new contributor has applied for this project -> {doc.get('interested_project')}",
                    "subject": "[CONTRIBUTOR-ENTRY] New Contributor Applied",
                }
            },
        ).start()

        return JsonResponse(data={}, status=201)


class Maintainer(APIView):
    """
    Maintainer API to Allow addition of maintainers to the database
    """

    throttle_classes = [PostThrottle]

    @staticmethod
    def _trigger_sns(validate):
        service.sns(
            payload={
                "message": f'Porting new project {validate.get("project_id")}\n \
                                    Details: \n \
                                    Name: {validate.get("name")} \n \
                                    Email Personal: {validate.get("email")} \n \
                                    Project Details: \n \
                                    Name: {validate.get("project_name")} \n \
                                    Description: {validate.get("description")}',
                "subject": "[PROJECT-PORT]: https://githubsrm.tech",
            }
        )

    def post(self, request, **kwargs) -> JsonResponse:
        """Accept Maintainers

        Args:
            request

        Returns:
            Response
        """
        validate = CommonSchema(
            request.data, query_param=request.GET.get("role")
        ).valid()
        if "error" in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        if "project_id" in validate:
            details = open_entry_checks.validate_beta_maintainer(doc=validate)
            open_entry.enter_beta_maintainer(doc=request.data)

            email_status = service.wrapper_email(
                role="maintainer_received",
                data={
                    "name": validate["name"],
                    "project_name": details["project_name"],
                    "email": validate["email"],
                },
            )
            if not email_status:
                open_entry.beta_maintainer_reset_status(maintainer_id=id)
                return JsonResponse(data={}, status=500)

            Thread(
                target=service.sns,
                kwargs={
                    "payload": {
                        "message": f'New Beta Maintainer for Project ID {validate.get("project_id")}\n \
                    Details: \n \
                    Name: {validate.get("name")} \n \
                    Email Personal: {validate.get("email")}',
                        "subject": "[BETA-MAINTAINER]: https://githubsrm.tech",
                    }
                },
            ).start()
            return JsonResponse(data={}, status=201)

        open_entry_checks.check_existing_project(
            description=validate["description"],
            project_name=validate["project_name"],
            project_url=validate["project_url"],
        )

        maintainer_details = open_entry.enter_maintainer(validate)
        (
            validate["project_id"],
            maintainer_id,
            validate["project_name"],
            validate["description"],
        ) = maintainer_details

        if validate.get("project_url"):
            Thread(target=self._trigger_sns, kwargs={"validate": validate}).start()

        email_status = service.wrapper_email(
            role="project_submission_confirmation",
            data={
                "project_name": validate["project_name"],
                "name": validate["name"],
                "project_description": validate["description"],
                "email": validate["email"],
            },
        )
        if not email_status:
            open_entry.alpha_maintainer_reset_status(
                project_id=validate.get("project_id"), maintainer_id=maintainer_id
            )
            return JsonResponse({}, status=500)

        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f'New Alpha Maintainer for Project ID {validate.get("project_id")}\n \
                        Details: \n \
                        Name: {validate.get("name")} \n \
                        Email Personal: {validate.get("email")} \n \
                        Project Details: \n \
                        Name: {validate.get("project_name")} \n \
                        Description: {validate.get("description")}',
                    "subject": "[ALPHA-MAINTAINER]: https://githubsrm.tech",
                }
            },
        ).start()
        return JsonResponse(data={}, status=201)

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
        if "error" in validate:
            return JsonResponse(data={"error": validate.get("error")}, status=400)

        open_entry.enter_contact_us(doc=request.data)

        Thread(
            target=service.sns,
            kwargs={
                "payload": {
                    "message": f'New Query Received! \n Name:{validate.get("name")} \n \
                Email: {validate.get("email")} \n \
                Message: {validate.get("message")} \n \
                Phone Number: {validate.get("phone_number")}',
                    "subject": "[QUERY]: https://githubsrm.tech",
                }
            },
        ).start()

        return JsonResponse(data={"success": True}, status=201)


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
        return JsonResponse(
            {"uptime": uptime, "status": "OK", "timeStamp": time.time()}, status=200
        )
