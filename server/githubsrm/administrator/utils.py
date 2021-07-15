from math import ceil
from typing import Dict

from apis import open_entry
from django.http import response
from rest_framework import status

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
    except:
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
            "error": "page does not exist"
        }, status=400)
