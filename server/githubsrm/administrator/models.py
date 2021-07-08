import pymongo
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()


class AdminEntry:
    def __init__(self) -> None:
        """
        Connect to mongodb
        """

        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def check_webHook(self, auth_header: str):
        """Checks for available webHook Token

        Args:
            token (str): token sent as header
        """
        try:
            token = auth_header.split()
            assert token[0] == "Bearer"
            if self.db.webHook.find_one({"token": token[1]}):
                return True
        except Exception as e:
            return
