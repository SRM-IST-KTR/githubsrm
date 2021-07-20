
from hashlib import sha256
from typing import Iterable, Dict, Any
import pymongo
from django.conf import settings
from apis import service
from administrator import jwt_keys


class Entry:
    def __init__(self) -> None:
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def approve_contributor(self, project_id: str, contributor_id: str) -> Any:
        """Maintainer approve contributor

        Args:
            project_id (str): project id
            contributor_id (str): contributor id

        Returns:
            bool
        """

        contributor = self.db.contributor.find_one_and_update(
            {"_id": contributor_id, "interested_project": project_id},
            update={
                "$set": {"is_maintainer_approved": True}
            }
        )

        if contributor:
            if contributor.get("is_maintainer_approved") and contributor.get("is_admin_approved"):
                return False
            project_doc = self.db.project.find_one_and_update(
                {"_id": project_id},
                update={
                    "$addToSet": {
                        "contributor_id": contributor_id
                    }
                }
            )
            return {**project_doc, **contributor}

        return False

    def find_Maintainer_credentials_with_email(self, email: str) -> Dict[str, Any]:
        """To find maintainer with email

        Args:
            email

        Returns:
            Dict
        """
        return self.db.maintainer_credentials.find_one({"email": email})

    def find_Maintainer_with_email(self, email: str) -> Dict[str, Any]:
        """To find maintainer with email

        Args:
            email

        Returns:
            Dict
        """
        return self.db.maintainer.find_one({"email": email})

    def find_all_Maintainer_with_email(self, email) -> Iterable:
        """To find maintainer with email

        Args:
            email

        Returns:
            Iterable
        """
        return self.db.maintainer.find({"email": email})

    def set_password(self, key: str, password: str) -> bool:
        """Set maintainer password

        Args:
            key (str): jwt key obtained from request
            password (str): new password

        Returns:
            bool:
        """

        decode = jwt_keys.verify_key(key=key)
        if decode:
            if "email" not in decode:
                return False

            maintainer = self.db.maintainer_credentials.find_one_and_update({
                "$and": [
                    {"email": decode.get("email")},
                    {"reset": True}
                ]
            }, update={
                "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
            })

            if maintainer:
                return True
            return False
        return False
