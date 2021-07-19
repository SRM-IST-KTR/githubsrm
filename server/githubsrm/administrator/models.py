import secrets
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict

import pymongo
from django.conf import settings
from dotenv import load_dotenv
from pymongo import ReturnDocument

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

    def find_maintainer_for_approval(self, maintainer_id: str, project_id: str) -> bool:
        """find and approve maintainer

        Args:
            maintainer_id (str): maintainer identifier
            project_id (str): project identifier

        Returns:
            bool
        """

        maintainer = self.db.maintainer.find_one_and_update(
            {"_id": maintainer_id, "project_id": project_id},
            update={
                "$set": {"is_admin_approved": True, "time_stamp": str(datetime.strftime(datetime.now(), format="%Y-%m-%d"))}
            }, return_document=ReturnDocument.BEFORE)

        if maintainer:
            if maintainer.get('is_admin_approved'):
                return False
            project = self._update_project(project_id=project_id,
                                           maintainer_id=maintainer_id)
            return project, maintainer
        return False

    def _update_project(self, project_id: str, maintainer_id: str) -> bool:
        """Update the project collection when a maintainer is added.

        Args:
            project_id (str): project identifier
            maintainer_id (str): maintainer identifier

        Returns:
            bool
        """

        project = self.db.project.find_one_and_update({"_id": project_id}, update={
            "$addToSet": {
                "maintainer_id": maintainer_id
            }
        }, return_document=ReturnDocument.AFTER)

        return project

    def check_existing_maintainer(self, email: str) -> bool:
        """Check for existing maintainer to determine if new keys are generated of
           or old keys are used.

        Args:
            email (str): maintainer email id

        Returns:
            bool: [description]
        """

        credentials = self.db.maintainer_credentials.find_one({
            "email": email
        })

        if credentials:
            return credentials.get("password")
        return False

    def get_random_password(self, email: str, length: int = 5) -> str:
        """Generating random passwords for maintainers and
           store in the maintainer credentials collection.

        Args:
            length (int, optional): byte length. Defaults to 5.
            email (str): maintainer email

        Returns:
            str
        """
        password = str(secrets.token_hex(length))

        doc = {"email": email,
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)

        return password

    def approve_project(self, identifier: str, project_url: str, private: bool) -> bool:
        """Approve project and update the doc as required

        Args:
            identifier (str): project id
            project_url (str): project url
            private (bool): visibility status

        Returns:
            bool
        """

        project = self.db.project.find_one_and_update(
            {"_id": identifier},
            update={
                "$set": {
                    "is_admin_approved": True,
                    "project_url": project_url,
                    "private": private
                }
            }, return_document=ReturnDocument.BEFORE)

        maintainer = self.db.maintainer.find_one({"project_id": identifier})

        if project:
            if project.get("is_admin_approved"):
                return False

            return project, maintainer

        return False

    def approve_contributor(self, project_id: str, contributor_id: str) -> bool:
        """Approve contributor to project.

        Args:
            project_id (str): project id
            contributor_id (str): contributor id

        Returns:
            bool: [description]
        """
        contributor = self.db.contributor.find_one_and_update(
            {"_id": contributor_id, "interested_project": project_id},
            update={
                "$set": {"is_admin_approved": True}
            }, return_document=ReturnDocument.BEFORE
        )
        if contributor:
            # Already approved
            if contributor.get("is_admin_approved"):
                return False

            project = self.db.project.find_one(
                {"_id": contributor["interested_project"]})
            return contributor, project

        return False

    def reset_status_maintainer(self, identifier: str, project_id: str) -> bool:
        """On failed email reset maintainer state

        Args:
            identifier (str) : maintainer id
            project_id (str) : project id
        Returns:
            bool
        """
        self.db.maintainer.find_one_and_update({
            "_id": identifier
        }, update={
            "$set": {"is_admin_approved": False}
        })

        self.db.project.find_one_and_update({
            "_id": project_id
        }, update={
            "$pull": {
                "maintainer_id": identifier
            }
        })

        return True

    def reset_status_project(self, project: Dict[str, Any]) -> bool:
        """Reset project status

        Args:
            project (Dict[str, Any]): project document

        Returns:
            bool
        """

        project = self.db.project.find_one_and_update({
            "_id": project["_id"]
        }, update={
            "$set": {
                "is_admin_approved": False,
                "project_url": project["project_url"],
                "private": project["private"]
            }
        }, return_document=ReturnDocument.BEFORE)

        if project:
            return True

        return False

    def reset_status_contributor(self, contributor: Dict[str, Any]) -> bool:
        """Reset contributor status

        Args:
            contributor (Dict[str, Any]): contributor document

        Returns:
            bool
        """

        self.db.contributor.find_one_and_update({
            "_id": contributor["_id"]
        }, update={
            "$set": {"is_admin_approved": False}
        })

        return True

    def get_all_maintainer_emails(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Get all maintainer emails from projects

        Args:
            project (Dict[str, Any]): project document

        Returns:
            Dict[str, Any]: list of all maintainer emails
        """
        try:
            maintainer_ids = project["maintainer_id"]
            maintainers = list(self.db.maintainer.find({
                "_id": {"$in": maintainer_ids}
            }))

        except Exception as e:
            return 

        doc = {}

        doc["email"] = [maintainer["email"] for maintainer in maintainers]

        return doc

    def get_maintainer_email(self, identifier: str) -> str:
        """Get maintainer email from identifier

        Args:
            identifier (str): maintainer id

        Returns:
            str: email
        """

        maintainer = self.db.maintainer.find_one({"_id": identifier})
        if maintainer:
            return maintainer["email"]

        return False
