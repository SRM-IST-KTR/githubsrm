from math import ceil
from typing import Any, Dict
import jwt
from . import entry
entry = entry.db


ITEMS_PER_PAGE = 10


def decode_payload(token):
    return jwt.decode(token, options={"require": ["exp"], "verify_signature": False}, algorithms=["HS256"])


def project_pagination(request, **kwargs):

    try:
        page = int(request.GET["page"])
        projects_ids = decode_payload(
            request.headers["Authorization"].split()[1])["project_id"]
        totalItems = entry.project.count_documents(
            {"_id": {"$in": projects_ids}})
        record = list(entry.project.aggregate([
            {"$match": {"_id": {"$in": projects_ids}}},
            {"$skip": (page - 1) * ITEMS_PER_PAGE},
            {"$limit": ITEMS_PER_PAGE},
        ]))
        if len(record) != 0:
            return {
                "currentPage": page,
                "hasNextPage": ITEMS_PER_PAGE * page < totalItems,
                "hasPreviousPage": page > 1,
                "nextPage": page + 1,
                "previousPage": page - 1,
                "lastPage": ceil(totalItems / ITEMS_PER_PAGE),
                "records": record
            }
        raise Exception()
    except Exception as e:
        print(e)
        return {"error": "Page does not exist"}


def project_single_project(request, **kwargs) -> Dict[str, Any]:
    """Get a specific project with all maintainer details and contributor details if they are approved

    Args:
        request

    Returns:
        doc: project/maintainer/contributor
    """

    projects_ids = decode_payload(
        request.headers["Authorization"].split()[1])["project_id"]
    project_id = request.GET["projectId"]

    page_maintainer, page_contributor = request.GET.get(
        "maintainer"), request.GET.get("contributor")

    if project_id not in projects_ids:
        return {"error": "wrong ID"}

    project = entry.project.find_one({"_id": project_id})
    if project:
        try:
            if page_maintainer:
                maintainers = entry.maintainer.aggregate(pipeline=[
                    {"$match": {"project_id": project_id}},
                    {"$skip": (page_maintainer-1) * ITEMS_PER_PAGE},
                    {"$limit": ITEMS_PER_PAGE}
                ])

                if maintainers:
                    project["maintainer"] = maintainers
                else:
                    raise

            if page_contributor:
                contributors = entry.contributor.aggregate(pipeline=[
                    {"$match": {"interested_project": project_id}},
                    {"$skip": (page_maintainer-1) * ITEMS_PER_PAGE},
                    {"$limit": ITEMS_PER_PAGE}
                ])

                if contributors:
                    project["contributor"] = contributors

                else:
                    raise
        except Exception as e:
            return {
                "error": "contributor and maintainers not found"
            }    

        return project
    
    return {
        "error": "project not found"
    }
