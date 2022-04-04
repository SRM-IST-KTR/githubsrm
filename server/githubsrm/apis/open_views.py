import json
from threading import Thread

from bson import json_util
from core.aws import service
from core.settings import PostThrottle
from core.utils import api_view
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from apis import open_entry, open_entry_checks

from .definitions import CommonSchema, ContactUsSchema


class Contributor(APIView):
    """
    Contributors API Allows additon of contributors to the database
    """

    throttle_classes = [PostThrottle]

    def post(self, request) -> JsonResponse:
        validate = CommonSchema(
            request.data, query_param=request.GET.get("role")
        ).valid()

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

    def post(self, request) -> JsonResponse:
        validate = CommonSchema(
            request.data, query_param=request.GET.get("role")
        ).valid()

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
            Thread(
                target=service.sns,
                kwargs={
                    "payload": {
                        "message": f'Porting new project {validate.get("project_id")}\n \
                                    Details: \n \
                                    Name: {validate.get("name")} \n \
                                    Email Personal: {validate.get("email")} \n \
                                    Project Details: \n \
                                    Name: {validate.get("project_name")} \n \
                                    Description: {validate.get("description")}',
                        "subject": "[PROJECT-PORT]: https://githubsrm.tech",
                    }
                },
            ).start()

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

    def get(self, request) -> JsonResponse:
        result = json.loads(json_util.dumps(open_entry.get_projects()))
        return JsonResponse(data=result, status=200, safe=False)


def catch_all(request, path=None):
    return redirect("https://githubsrm.tech")


@api_view(["GET"])
def team(request) -> JsonResponse:
    result = json.loads(json_util.dumps(open_entry.get_team_data()))
    return JsonResponse(result, status=200, safe=False)


@api_view(["POST"])
def contact_us(request) -> JsonResponse:
    validate = ContactUsSchema(data=request.data).valid()
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
