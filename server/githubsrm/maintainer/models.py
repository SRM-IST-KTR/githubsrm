
from typing import Iterable
import pymongo
from django.conf import settings


class Entry:
    db = None

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

    def Send_all_Maintainer_email(self, email) -> Iterable:
        return self.db.maintainer.find({"email": email})
