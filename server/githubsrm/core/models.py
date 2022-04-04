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
        # Todo: Find more efficient way for 4 byte uuid generation
        gen_id = random.choices(string.ascii_uppercase + string.digits, k=8)

        if (
            self.db.project.find_one({"_id": gen_id})
            or self.db.contributor.find_one({"_id": gen_id})
            or self.db.maintainer.find_one({"_id": gen_id})
        ):
            return self.get_uid()

        return "".join(gen_id)
