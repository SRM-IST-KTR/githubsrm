from typing import Any, Dict
from hashlib import sha256
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

    def insert_admin(self, doc: Dict[str, str]) -> bool:
        """Insert admin details.

        Args:
            doc (Dict[str, str]): document send in from request body

        Returns:
            bool

        """
        if self.db.admins.find_one({"email": doc.get('email')}):
            return False
        try:
            password = doc.pop('password')
            hash_password = sha256(password.encode()).hexdigest()

            doc = {**doc, **{"password": hash_password}}
            self.db.admins.insert_one(document=doc)
            return True
        except Exception as e:
            return False

    def verify_admin(self, email: str, password: str) -> bool:
        """Verify admin users

        Args:
            identifier (str): entred password

        Returns:
            bool
        """
        hash_password = sha256(password.encode()).hexdigest()
        if value := self.db.admins.find_one({
            "$and": [
                {"password": hash_password},
                {"email": email}
            ]
        }):
            return value
        return False
