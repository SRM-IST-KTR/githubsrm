import binascii
import hashlib
import os
import secrets
from datetime import datetime
from threading import Thread
from typing import Any, Dict, Tuple

from core import service
from core.errorfactory import ProjectErrors
from core.models import BaseModel
from pymongo import ReturnDocument

from .errors import (
    ContributorApprovedError,
    ContributorNotFoundError,
    ExistingAdminError,
    InvalidAdminCredentialsError,
    InvalidWebhookError,
    MaintainerApprovedError,
    MaintainerNotFoundError,
    ProjectNotFoundError,
)


class AdminEntry(BaseModel):
    def __init__(self) -> None:
        super().__init__()

    def check_webHook(self, token: Tuple):
        """Checks for available webHook Token

        Args:
            token (Tuple): token sent as header
        """
        token_type, token = token
        if token_type != "Bearer":
            raise InvalidWebhookError(detail={"error": "Invalid token type"})
        webHook = self.db.webHook.find_one({"token": token})
        if webHook:
            return True
        raise InvalidWebhookError(detail={"error": "Invalid token"})

    def hash_password(self, password: str) -> str:
        """Hashes password using salted password hashing (SHA512 & PBKDF_HMAC2)
        Args:
            password : Password to be hashed

        Returns:
            str : Hashed password
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwd_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode("ascii")
        return final_hashed_pwd

    def insert_admin(self, doc: Dict[str, str]) -> bool:
        """Insert admin details.

        Args:
            doc (Dict[str, str]): document send in from request body

        Returns:
            bool

        """
        if self.db.admins.find_one({"email": doc.get("email")}):
            raise ExistingAdminError()
        password = doc.pop("password")
        password_hash = self.hash_password(password)

        doc = {**doc, **{"password": password_hash}}
        self.db.admins.insert_one(document=doc)

    def verify_admin(self, email: str, password: str) -> bool:
        """Verify admin users

        Args:
            identifier (str): entred password

        Returns:
            bool
        """
        if value := self.db.admins.find_one({"email": email}):
            dbpwd = value["password"]
            salt = dbpwd[:64]
            dbpwd = dbpwd[64:]
            pwd_hash = hashlib.pbkdf2_hmac(
                "sha512", password.encode("utf-8"), salt.encode("ascii"), 100000
            )
            pwd_hash = binascii.hexlify(pwd_hash).decode("ascii")
            if pwd_hash == dbpwd:
                return value
        raise InvalidAdminCredentialsError()

    def find_maintainer_for_approval(
        self, maintainer_id: str, project_id: str, maintainer_email: str
    ) -> bool:
        """find and approve maintainer

        Args:
            maintainer_id (str): maintainer identifier
            project_id (str): project identifier
            maintainer_email (str): maintainer_email

        Returns:
            bool
        """

        maintainer = self.db.maintainer.find_one_and_update(
            {"_id": maintainer_id, "project_id": project_id, "email": maintainer_email},
            update={
                "$set": {
                    "is_admin_approved": True,
                    "time_stamp": str(
                        datetime.strftime(datetime.now(), format="%Y-%m-%d")
                    ),
                }
            },
            return_document=ReturnDocument.BEFORE,
        )

        if maintainer:
            if maintainer.get("is_admin_approved"):
                raise MaintainerApprovedError()
            project = self._update_project(
                project_id=project_id, maintainer_id=maintainer_id
            )
            return project, maintainer
        raise MaintainerNotFoundError(detail={"error": "Maintainer not found"})

    def _update_project(self, project_id: str, maintainer_id: str) -> bool:
        """Update the project collection when a maintainer is added.

        Args:
            project_id (str): project identifier
            maintainer_id (str): maintainer identifier

        Returns:
            bool
        """

        project = self.db.project.find_one_and_update(
            {"_id": project_id},
            update={"$addToSet": {"maintainer_id": maintainer_id}},
            return_document=ReturnDocument.AFTER,
        )

        return project

    def check_existing_maintainer(self, email: str) -> bool:
        """Check for existing maintainer to determine if new keys are generated of
           or old keys are used.

        Args:
            email (str): maintainer email id

        Returns:
            bool: [description]
        """

        credentials = self.db.maintainer_credentials.find_one({"email": email})

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

        doc = {"email": email, "password": password, "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)

        return password

    def get_maintainer_github_id(self, maintainer_ids: list):
        """get github ids from maintainer document

        Args:
            maintainer_ids (list): maintainer id list
        """
        val = []
        if maintainers := list(
            self.db.maintainer.find(filter={"_id": {"$in": maintainer_ids}})
        ):
            for maintainer in maintainers:
                val.append(maintainer["github_id"])
            return val
        else:
            return False

    def approve_project(self, identifier: str, year: str) -> bool:
        """Approve project and update the doc as required

        Args:
            identifier (str): project id
            academic_year (str): academic_year

        Returns:
            bool
        """
        project_doc = self.db.project.find_one(filter={"_id": identifier})
        if project_doc:
            maintainer_github_id = self.get_maintainer_github_id(
                project_doc["maintainer_id"]
            )
            submission = {
                **{"project-name": project_doc["project_name"]},
                **{"project-description": project_doc["description"]},
                **{"year": year},
                **{"private": project_doc["private"]},
                **{"maintainers": maintainer_github_id},
            }
            response = service.lambda_(func="githubcommunitysrm-v1", payload=submission)

            if response["success"] and project_doc["is_admin_approved"] == False:
                project = self.db.project.find_one_and_update(
                    {"_id": identifier},
                    update={
                        "$set": {
                            "is_admin_approved": True,
                            "year": year,
                            "team_slug": response["team-slug"],
                            "private": response["private"],
                            "project_url": response["repo-link"],
                        }
                    },
                    return_document=ReturnDocument.BEFORE,
                )
                project = {**project, **{"project_url": response["repo-link"]}}
                return project
            else:
                if response["success"] == False:
                    Thread(
                        target=service.sns,
                        kwargs={
                            "payload": {
                                "message": "Lambda returned success false",
                                "subject": "Lambda failed",
                            }
                        },
                    ).start()
                raise ProjectErrors(detail={"error": "Lambda returned success False"})
        raise ProjectNotFoundError()

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
            update={"$set": {"is_admin_approved": True}},
            return_document=ReturnDocument.BEFORE,
        )
        if contributor:
            # Already approved
            if contributor.get("is_admin_approved"):
                raise ContributorApprovedError(
                    detail={"error": "Contributor already approved"}
                )

            project = self.db.project.find_one(
                {"_id": contributor["interested_project"]}
            )
            return contributor, project

        raise ContributorNotFoundError({"error": "Contributor/Project not found"})

    def reset_status_maintainer(self, identifier: str, project_id: str) -> bool:
        """On failed email reset maintainer state

        Args:
            identifier (str) : maintainer id
            project_id (str) : project id
        Returns:
            bool
        """
        self.db.maintainer.find_one_and_update(
            {"_id": identifier}, update={"$set": {"is_admin_approved": False}}
        )

        self.db.project.find_one_and_update(
            {"_id": project_id}, update={"$pull": {"maintainer_id": identifier}}
        )

        return True

    def reset_status_project(self, project: Dict[str, Any]) -> bool:
        """Reset project status

        Args:
            project (Dict[str, Any]): project document

        Returns:
            bool
        """

        project = self.db.project.find_one_and_update(
            {"_id": project["_id"]},
            update={
                "$set": {
                    "is_admin_approved": False,
                    "project_url": "",
                    "team_slug": "",
                    "year": "",
                }
            },
            return_document=ReturnDocument.BEFORE,
        )

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

        self.db.contributor.find_one_and_update(
            {"_id": contributor["_id"]}, update={"$set": {"is_admin_approved": False}}
        )

        return True

    def admin_remove_maintainer(self, identifier: str) -> bool:
        """Admin remove maintainer

        Args:
            identifier (str): maintainer id

        Returns:
            bool:
        """

        maintainer = self.db.maintainer.find_one_and_delete(
            {"_id": identifier, "is_admin_approved": False}
        )

        if not maintainer:
            return False

        project_id = maintainer["project_id"]

        project_name = self.db.project.find_one({"_id": project_id})["project_name"]

        project = self.db.project.find_one_and_delete(
            {"_id": project_id, "maintainer_id": {"$exists": False}}
        )

        maintainer["project_name"] = project_name

        if maintainer:
            return maintainer
        else:
            return False

    def admin_remove_contributor(self, identifier: str) -> str:
        """Admin remove contributor

        Args:
            identifier (str): contirbutor id

        Returns:
            str: Removal status
        """

        contributor = self.db.contributor.find_one_and_delete(
            {
                "_id": identifier,
                "is_maintainer_approved": False,
                "is_admin_approved": False,
            }
        )

        if contributor:
            project_name = self.db.project.find_one(
                {"_id": contributor["interested_project"]}
            )["project_name"]
            contributor["project_name"] = project_name
            return contributor
        else:
            return False

    def get_all_maintainer_emails(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Get all maintainer emails from projects

        Args:
            project (Dict[str, Any]): project document

        Returns:
            Dict[str, Any]: list of all maintainer emails
        """
        try:
            maintainer_ids = project["maintainer_id"]
            maintainers = list(
                self.db.maintainer.find({"_id": {"$in": maintainer_ids}})
            )
        except Exception:
            return
        return dict(email=[maintainer["email"] for maintainer in maintainers])

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
