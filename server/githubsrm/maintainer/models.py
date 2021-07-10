
import pymongo
from django.conf import settings
from pymongo.database import Database
# Create your models here.


def ConnectDB() -> Database:
    client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
    return client[settings.DATABASE['db']]
