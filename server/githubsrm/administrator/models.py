import pymongo
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class AdminEntry:
    def __init__(self) -> None:
        """
        Connect to mongodb
        """

        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def check_webHook(self, token: str):
        """Checks for available webHook Token

        Args:
            token (str): token sent as header
        """
        try:
            if self.db.webHook.find_one({"token": token}):
                return True
        except Exception as e:
            return False
