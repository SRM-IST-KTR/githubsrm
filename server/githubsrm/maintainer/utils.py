import re
from pymongo import message
from . import db


def Projects_pagnation(request, **kwargs):
   return "Page does not exist"









def project_SingleProject(request, **kwargs):
    """
        Get a specific project with all maintainer details and contributor details if they are approved
    """

    # TODO check from JWT that this project id is in it as well

    project_id = request.GET["projectId"]
    if project_document := db.project.find_one({"_id": project_id}):

        # TODO add a sanity check here -> array length in project contributor_id and maintainer_id
        # * is SAME as the number of documents in maintainer and contributor collections with the
        # * same id and is_approved : true

        # * will have atleast one maintainer (ALPHA)
        if request.GET["maintainer"] == "true":
            data = list(db.maintainer.find(
                {"project_id": project_id, "is_admin_approved": True}))
            project_document["maintainer"] = data

        if request.GET["contributor"] == "true":
            data = list(db.contributor.find(
                {"project_id": project_id, "is_admin_approved": True}))
            project_document["contributor"] = data
    else:
        return "id doesnt exist"

    return project_document
