from typing import Dict
from rest_framework import status
from math import ceil
from .models import AdminEntry
from django.http import response
from apis import openEntry


def project_Pagination(request, **kwargs):
    """
        Send paginated projects here

        Using values from query params for page number

        Args:
            request

        Returns:
            response.Response
    """
    ITEMS_PER_PAGE = 10
    try:
        page = int(request.GET["page"])
        entry=openEntry
        totalItems = entry.db.project.count_documents({})
        record = list(entry.db.project.aggregate([
            {"$skip": (page - 1) * ITEMS_PER_PAGE},
            {"$limit": ITEMS_PER_PAGE},
        ]))
        if len(record) != 0:
            return response.JsonResponse({
                "currentPage": page,
                "hasNextPage": ITEMS_PER_PAGE * page < totalItems,
                "hasPreviousPage": page > 1,
                "nextPage": page + 1,
                "previousPage": page - 1,
                "lastPage": ceil(totalItems / ITEMS_PER_PAGE),
                "records": record
            }, status=status.HTTP_200_OK)
        raise Exception()
    except:
        return response.JsonResponse({"error": "Page does not exist"}, status=status.HTTP_400_BAD_REQUEST)


def project_SingleProject(request, **kwargs):
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

        if request.GET["maintainer"] != "true" and request.GET["contributor"] != "true":
            record = {"project": project}

        elif request.GET["maintainer"] == "true" and request.GET["contributor"] != "true":
            data = list(entry.db.maintainer.find(
                {"project_id": request.GET["projectId"]}))
            record = {"maintainer": data}

        elif request.GET["maintainer"] != "true" and request.GET["contributor"] == "true":
            data = list(entry.db.contributor.find(
                {"project_id": request.GET["projectId"]}))
            record = {"contributor": data}

        else:
            maintainerData = list(entry.db.maintainer.find(
                {"project_id": request.GET["projectId"]}))
            contributorData = list(entry.db.contributor.find(
                {"project_id": request.GET["projectId"]}))
            record = {"maintainer": maintainerData,
                      "contributor": contributorData}

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
