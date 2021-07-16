
from hashlib import sha256
from typing import Dict, Iterable
import pymongo
from django.conf import settings
from pymongo.database import Database


class Entry:
    def __init__(self) -> None:
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def approve_contributor(self, project_id: str, contributor_id: str) -> bool:
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
            self.db.project.find_one_and_update(
                {"_id": project_id},
                update={
                    "$addToSet": {
                        "contributor_id": contributor_id
                    }
                }
            )
            return True

        return False

    def find_Maintainer_with_email(self, email) -> Dict:
        """To find maintainer with email

        Args:
            email

        Returns:
            Iterable
        """
        return self.db.maintainer_credentials.find_one({"email": email})

    def find_all_Maintainer_with_email(self, email) -> Iterable:
        """To find maintainer with email

        Args:
            email

        Returns:
            Iterable
        """
        return self.db.maintainer.find({"email": email})

    def update_password(self, current_password: str, new_password: str,
                        maintainer_email: str) -> bool:
        """Change password if current_password is correct

        Args:
            current_password (str): current maintainer password
            new_password (str): new maintainer password
            maintainer_email (str): srm email
        Returns:
            bool
        """

        current_password = sha256(current_password.encode()).hexdigest()
        new_password = sha256(new_password.encode()).hexdigest()

        verify = self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": maintainer_email},
                {"password": current_password}
            ]
        }, update={
            "$set": {"password": new_password}
        })

        if verify:
            return True

        return False
