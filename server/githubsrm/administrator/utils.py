from math import ceil
from threading import Thread
from typing import Dict

from apis import open_entry, service
from django.http import response
from rest_framework import status

from administrator import entry
from maintainer.utils import RequestSetPassword
from .models import AdminEntry

ITEMS_PER_PAGE = 10


def project_pagination(request, **kwargs):
    """
        Send paginated projects here

        Using values from query params for page number

        Args:
            request

        Returns:
            response.Response
    """
    try:
        page = int(request.GET["page"])
        entry = open_entry
        total_docs = entry.db.project.count_documents({})
        records = list(entry.db.project.aggregate([
            {"$skip": (page - 1) * ITEMS_PER_PAGE},
            {"$limit": ITEMS_PER_PAGE},
        ]))
        if len(records) != 0:
            return response.JsonResponse({
                "currentPage": page,
                "hasNextPage": ITEMS_PER_PAGE * page < total_docs,
                "hasPreviousPage": page > 1,
                "nextPage": page + 1,
                "previousPage": page - 1,
                "lastPage": ceil(total_docs / ITEMS_PER_PAGE),
                "records": records
            }, status=status.HTTP_200_OK)
        raise Exception()
    except:
        return response.JsonResponse({"error": "Page does not exist"}, status=status.HTTP_400_BAD_REQUEST)


def project_single_project(request, **kwargs):
    """
        Send single project but detailed

        Args:
            request

        Returns:
            response.JsonResponse
    """
    entry = AdminEntry()
    try:
        project = entry.db.project.find_one(
            {"_id": request.GET["projectId"]})
        if not project:
            raise Exception("Project doesn't exist")

        record = {"project": project}

        if request.GET["maintainer"] == "true" and request.GET["contributor"] != "true":
            data = list(entry.db.maintainer.find(
                {"project_id": request.GET["projectId"]}))
            record["maintainer"] = {"maintainer": data}

        elif request.GET["maintainer"] != "true" and request.GET["contributor"] == "true":
            data = list(entry.db.contributor.find(
                {"interested_project": request.GET["projectId"]}))
            record["contributor"] = {"contributor": data}

        else:
            maintainerData = list(entry.db.maintainer.find(
                {"project_id": request.GET["projectId"]}))
            contributorData = list(entry.db.contributor.find(
                {"interested_project": request.GET["projectId"]}))

            record["maintainer"] = {"maintainer": maintainerData}
            record["contributor"] = {"contributor": contributorData}

        return response.JsonResponse(record, status=status.HTTP_200_OK)
    except Exception as e:
        return response.JsonResponse(
            {"error": "Project doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


def get_token(request_header: Dict[str, str]):
    try:
        token = request_header.get('Authorization').split()

        return token[0], token[1]
    except Exception as e:
        return False


def accepted_project_pagination(request, **kwargs) -> response.JsonResponse:
    """Get all accepted project

    Args:
        request 

    Returns:
        response.JsonResponse
    """

    try:
        page = int(request.GET.get("page"))
        total_docs = open_entry.db.project.count_documents(
            {"is_admin_approved": True})

        records = list(open_entry.db.project.aggregate([
            {"$match": {"is_admin_approved": True}},
            {"$skip": (page - 1) * ITEMS_PER_PAGE},
            {"$limit": ITEMS_PER_PAGE},
        ]))

        if len(records) != 0:
            return response.JsonResponse({
                "currentPage": page,
                "hasNextPage": ITEMS_PER_PAGE * page < total_docs,
                "hasPreviousPage": page > 1,
                "nextPage": page + 1,
                "previousPage": page - 1,
                "lastPage": ceil(total_docs / ITEMS_PER_PAGE),
                "records": records
            }, status=status.HTTP_200_OK)

        raise Exception()

    except Exception as e:
        print(e)
        return response.JsonResponse({
            "hasNextPage": False,
            "hasPreviousPage": False,
            "record": []
        }, status=200)


def alpha_maintainer_support(existing: bool, project: Dict[str, str],
                             maintainer: Dict[str, str], request) -> Dict[str, str]:
    """Support for alpha maintainer flow

    Args:
        existing (bool): defines credentials state
        project (Dict[str, str]): project document
        maintainer (Dict[str, str]): maintainer document
        request: request object

    Returns:
        Dict[str, str]: response
    """
    if existing:
        if service.wrapper_email(
                role="project_submission_approval", data={
                    "name": maintainer["name"],
                    "project_name": project["project_name"],
                    "email": maintainer["email"],
                    "project_id": project["_id"]
                }):

            Thread(target=service.wrapper_email, kwargs={
                "role": "new_maintainer_notification",
                "data": {
                    "name": "Maintainer",
                    "email": request.data["email"],
                    "project_name": project["project_name"],
                    "beta_name": maintainer["name"],
                    "beta_email": maintainer["email"]
                }
            }).start()

            return {
                "message": {"success": "Approved existing maintainer"},
                "status": 200
            }

        else:
            entry.reset_status_maintainer(
                identifier=maintainer["_id"], project_id=project["_id"]
            )
            return {
                "message": {"error": "email failed"},
                "status": 500
            }
    else:
        password = RequestSetPassword(email=request.data.get("email"))
        if service.wrapper_email(
                role="project_submission_approval_w_password_link", data={
                    "name": maintainer["name"],
                    "project_name": project["project_name"],
                    "reset_token": password,
                    "email": maintainer["email"],
                    "project_id": project["_id"],
                }):
            return {
                "message": {"success": "Approved new maintainer"},
                "status": 200
            }

        else:
            entry.reset_status_maintainer(
                identifier=maintainer["_id"], project_id=project["_id"]
            )

            return {
                "message": {"error": "email failed"},
                "status": 500
            }


def beta_maintainer_support(existing: bool, project: Dict[str, str],
                            maintainer: Dict[str, str], request) -> Dict[str, str]:
    """Support for beta maintainer flow

    Args:
        existing (bool): is existing beta maintainer
        project (Dict[str, str]): project document
        maintainer (Dict[str, str]): maintainer document
        request

    Returns:
        Dict[str, str]: response
    """
    if existing:
        if service.wrapper_email(
                role="welcome_maintainer", data={
                    "name": maintainer["name"],
                    "project_name": project["project_name"],
                    "email": maintainer["email"]
                }):
            Thread(target=service.wrapper_email, kwargs={
                "role": "new_maintainer_notification",
                "data": {
                    "name": "Maintainer",
                    "email": request.data["email"],
                    "project_name": project["project_name"],
                    "beta_name": maintainer["name"],
                    "beta_email": maintainer["email"]
                }
            }).start()

            return {
                "message": {"success": "Approved existing maintainer"},
                "status": 200
            }

        else:
            entry.reset_status_maintainer(
                identifier=maintainer["_id"], project_id=project["_id"])

            return {
                "message": {"error": "email failed"},
                "status": 500
            }

    else:
        password = RequestSetPassword(email=request.data.get("email"))

        if service.wrapper_email(
                role="welcome_maintainer_w_password_link", data={
                    "name": maintainer["name"],
                    "project_name": project["project_name"],
                    "reset_token": password,
                    "email": maintainer["email"]
                }):
            Thread(target=service.wrapper_email, kwargs={
                "role": "new_maintainer_notification",
                "data": {
                    "name": "Maintainer",
                    "email": request.data["email"],
                    "project_name": project["project_name"],
                    "beta_name": maintainer["name"],
                    "beta_email": maintainer["email"]
                }
            }).start()

            return {
                "message": {"Approved new maintainer"},
                "status": 200
            }
        else:
            entry.reset_status_maintainer(
                identifier=maintainer["_id"], project_id=project["_id"]
            )

            return {
                "message": {"error": "email failed"},
                "status": 500
            }
