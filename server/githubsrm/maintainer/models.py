
import pymongo
from django.conf import settings
from pymongo.database import Database
# Create your models here.

class Entry:
    def __init___(self):
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]
