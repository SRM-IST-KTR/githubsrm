from math import ceil
import jwt
from . import entry
db = entry.db


def decode_payload(token):
    return jwt.decode(token, options={"require": ["exp"], "verify_signature": False}, algorithms=["HS256"])

def Projects_pagnation(request, **kwargs):

    ITEMS_PER_PAGE = 10
    try:
        page = int(request.GET["page"])
        projects_ids = decode_payload(
            request.headers["Authorization"].split()[1])["project_id"]
        totalItems = db.project.count_documents({"_id": {"$in": projects_ids}})
        record = list(db.project.aggregate([
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


def project_SingleProject(request, **kwargs):
    """
        Get a specific project with all maintainer details and contributor details if they are approved
    """

    projects_ids = decode_payload(
        request.headers["Authorization"].split()[1])["project_id"]
    project_id = request.GET["projectId"]

    if project_id not in projects_ids:
        return {"error": "wrong ID"}

    if project_document := db.project.find_one({"_id": project_id}):

        if request.GET["maintainer"] == "true":
            data = list(db.maintainer.find(
                {"project_id": project_id, "is_admin_approved": True}, {"password": 0}))
            project_document["maintainer"] = data

        if request.GET["contributor"] == "true":
            data = list(db.contributor.find(
                {"interested_project": project_id, "is_admin_approved": True}, {"password": 0}))
            project_document["contributor"] = data
    else:
        return {"error": "id doesnt exist"}

    return project_document
