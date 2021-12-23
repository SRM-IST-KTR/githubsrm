import random
import string

import pymongo
from django.conf import settings


class BaseModel:
    def __init__(self) -> None:
        """
        Connect to mongodb
        """

        client = pymongo.MongoClient(settings.DATABASE["mongo_uri"])
        self.db = client[settings.DATABASE["db"]]

    def get_uid(self) -> str:
        """Returns 8 character alpha numeric unique id

        Args:
            length (int)
            operator (pymongo.MongoClient)

        Returns:
            str
        """

        gen_id = random.choices(string.ascii_uppercase + string.digits, k=8)

        if self.db.collection.find_one({"_id": gen_id}):
            return self.get_uid(length=8)

        return "".join(gen_id)
