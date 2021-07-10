
import pymongo
from django.conf import settings
# Create your models here.


class Entry:
    db = None

    def __init__(self):
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]
        