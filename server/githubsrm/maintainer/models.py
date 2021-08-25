
from hashlib import sha256
from threading import Thread
from typing import Iterable, Dict, Any
import pymongo
from django.conf import settings
from administrator import jwt_keys

from apis.aws import BotoService

service = BotoService()


class Entry:
    def __init__(self) -> None:
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def _approve_contributor(self, contributor: Dict[str, str]):
        """Trigger lambda for contributor addition

        Args:
            contributor (Dict[str, str]): contirbutor details
        """
        project = self.db.project.find_one(
            filter={"_id": contributor["interested_project"]})
        submission = {
            **{"team-slug": project["team_slug"]}, **{"contributor": contributor["github_id"]}}
        response = service.lambda_(
            func="githubcommunitysrm-v2", payload=submission)

        if response["success"] == False:
            service.sns(payload={
                        "message": f"Lambda failing on contirbutor approval contributor_id -> {contributor['_id']} \
                         Error: {response}", "subject": "[LAMBDA-FAILING]"})
        else:
            self.db.contributor.find_one_and_update({"_id": contributor["_id"]}, update={
                "$set": {"is_added_to_repo": True}
            })

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
            Thread(target=self._approve_contributor, kwargs={
                   "contributor": contributor}).start()
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

    def find_contributor_for_removal(self, identifier: str, project_ids: list) -> Dict[str, Any]:
        """FInd contributors from contributor id

        Args:
            identifier (str): identifier
            project_ids (list): maintainer project ids

        Returns:
            Dict[str, Any]
        """
        if len(project_ids):
            contributor = self.db.contributor.find_one_and_delete({"_id": identifier,
                                                                   "is_admin_approved": True,
                                                                   "is_maintainer_approved": False,
                                                                   "interested_project": {"$in": project_ids}})
            project_name = self.db.project.find_one({
                "_id": contributor["interested_project"]
            })["project_name"]

            if contributor:
                contributor["project_name"] = project_name
                return contributor

        else:
            return False

    def remove_contributor(self, identifier: str) -> bool:
        """Remove contributor

        Args:
            identifier (str): contributor id

        Returns:
            bool
        """
        self.db.contributor.find_one_and_delete({"_id": identifier})
        return True

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

    def projects_from_email(self, email: str) -> list:
        """Get all projects from email

        Args:
            email (str): maintainer emails

        Returns:
            list: list of all projects
        """
        projects = self.db.maintainer.find({
            "email": email,
            "is_admin_approved": True
        }, {"name": 0, "email": 0, "srm_email": 0,
            "reg_number": 0, "branch": 0, "is_admin_approved": 0,
            "time_stamp": 0, "github_id": 0, "_id": 0})

        projects = list(projects)
        if len(projects):
            return [project["project_id"] for project in projects]
        return False
