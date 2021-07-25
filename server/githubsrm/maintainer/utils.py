import random
from math import ceil
from typing import Any, Dict
from administrator import jwt_keys
from administrator.utils import get_token
from . import entry

open_entry = entry
entry = entry.db

ITEMS_PER_PAGE = 10


def decode_payload(token: str) -> Dict[str, Any]:
    """Helper for jwt decode
    Args:
        token (str): jwt 
    Returns:
        Dict[str, Any]
    """
    return jwt_keys.verify_key(key=token)


def project_pagination(request, **kwargs):

    try:
        page = int(request.GET["page"])
        projects_ids = request.project_ids
        totalItems = request.total_items

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
        return {
            "hasNextPage": False,
            "hasPreviousPage": False,
            "records": []
        }


def project_single_project(request, **kwargs) -> Dict[str, Any]:
    """Get a specific project with all maintainer details and contributor details if they are approved
    Args:
        request
    Returns:
        doc: project/maintainer/contributor
    """
    try:

        projects_ids = decode_payload(
            get_token(request_header=request.headers))["project_id"]
        project_id = request.GET["projectId"]

    except Exception as e:
        return {
            "error": "inconsistant data"
        }

    maintainer_page, contributor_page = request.GET.get(
        "maintainer"), request.GET.get("contributor")

    if project_id not in projects_ids:
        return {"error": "wrong ID"}

    doc = entry.project.aggregate(
        get_pagnation_aggregate(project_id=project_id, count=True))

    doc = list(doc)

    maintainer_count = 0
    contributor_count = 0

    try:
        maintainer_count = doc[0]["maintainer"][0]["count"]
        contributor_count = doc[0]["contributor"][0]["count"]
    except Exception as e:
        pass

    try:
        docs = list(entry.project.aggregate(get_pagnation_aggregate(project_id=project_id, count=False,
                                                                    maintainer_page=maintainer_page, contributor_page=contributor_page,

                                                                    maintainer_docs=maintainer_count, contributor_docs=contributor_count)))
        docs = docs[0]
        docs["maintainerHasNextPage"] = (
            ITEMS_PER_PAGE * int(maintainer_page)) < int(maintainer_count)
        docs["contributorHasNextPage"] = (
            ITEMS_PER_PAGE * int(contributor_page)) < int(contributor_count)

    except Exception as e:
        return {
            "hasNextPage": False,
            "hasPreviousPage": False,
            "records": []
        }

    return docs


def get_pagnation_aggregate(count: bool, project_id, maintainer_docs=None, contributor_docs=None,
                            maintainer_page=None, contributor_page=None, ):

    doc = [{
        '$match': {'_id': project_id}
    },
        {
        '$lookup': {
            'from': 'maintainer',
            'pipeline': [
                    {
                        '$match': {'is_admin_approved': True, 'project_id': project_id}
                    }, {"$count": "count"}
            ],
            'as': 'maintainer'
        }
    },
        {
        '$lookup': {
            'from': 'contributor',
            'pipeline': [
                    {
                        '$match': {
                            'is_admin_approved': True,
                            'project_id': project_id
                        }
                    }, {"$count": "count"}
            ],
            'as': 'contributor'
        }
    }
    ]
    if count:
        return doc
    else:
        doc = [{
            '$match': {'_id': project_id}
        },
            {
            '$lookup': {
                'from': 'maintainer',
                'pipeline': [
                    {
                        '$match': {'is_admin_approved': True, 'project_id': project_id}
                    },
                    {"$skip": (int(maintainer_page)-1) * maintainer_docs}, {"$limit": ITEMS_PER_PAGE}],
                'as': 'maintainer'
            }
        },
            {
            '$lookup': {
                'from': 'contributor',
                'pipeline': [
                    {
                        '$match': {
                            'is_admin_approved': True,
                            'interested_project': project_id
                        }
                    }, {"$skip": (int(contributor_page)-1) * contributor_docs}, {"$limit": ITEMS_PER_PAGE}],

                'as': 'contributor'
            }
        }
        ]

    return doc


def RequestSetPassword(email):
    """
    When new user is created or when the user requests a change in password
    """
    document = entry.maintainer_credentials.find_one_and_update({
        "email": email
    }, update={
        "$set": {"reset": True}
    })
    expiry = 10
    if not document:
        doc = {
            "email": email,
            "password": "".join(random.choice("ABHISHEK") for i in range(10)),
            "reset": True
        }
        entry.maintainer_credentials.insert_one(doc)
        expiry = 168*60

    return jwt_keys.issue_key({"email": email}, expiry=expiry)
