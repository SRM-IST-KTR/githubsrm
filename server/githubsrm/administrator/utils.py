from rest_framework.views import APIView
from rest_framework import response, status
from dotenv import load_dotenv
import pymongo
from math import ceil
import os

load_dotenv()

def project_Pagination(request, **kwargs):
    """
        Send paginated projects here

        Using values from query params for page number

        Args:
            request

        Returns:
            response.Response
    """
    ITEMS_PER_PAGE=10
    values=list(request.GET.values())
    page=int(values[0])
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))

    db = client[os.getenv('MONGO_DB')]
    totalItems= db.project.count_documents({})
    record = list(db.project.aggregate([
        {"$skip": (page - 1) * ITEMS_PER_PAGE},
        {"$limit": ITEMS_PER_PAGE},
    ]))
    if len(record)!=0:
        return response.Response({
            "currentPage": page,
            "hasNextPage": ITEMS_PER_PAGE * page < totalItems,
            "hasPreviousPage": page > 1,
            "nextPage": page + 1,
            "previousPage": page - 1,
            "lastPage": ceil(totalItems / ITEMS_PER_PAGE),
            "records": record
        }, status=status.HTTP_200_OK)
    return response.Response("Page does not exist",status=status.HTTP_400_BAD_REQUEST)


def project_SingleProject(request, **kwargs):
    """
        Send single project but detailed
    """
    return response.Response(status=status.HTTP_200_OK)
