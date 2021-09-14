from hashlib import sha256
from .errors import (
    ContributorNotFoundError,
    ContributorApprovedError,
    ProjectErrors,
    MaintainerNotFoundError,
    AuthenticationErrors,
)
from threading import Thread
from typing import Iterable, Dict, Any
import pymongo
from django.conf import settings
from administrator import jwt_keys


import hashlib, binascii, os

from core import service


class Entry:
    def __init__(self) -> None:
        client = pymongo.MongoClient(settings.DATABASE["mongo_uri"])
        self.db = client[settings.DATABASE["db"]]

    def hash_password(self, password: str) -> str:
        """Hashes password using salted password hashing (SHA512 & PBKDF_HMAC2)
            Args:
                password : Password to be hashed
                
            Returns:
                str : Hashed password
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode('ascii')
        return final_hashed_pwd

    #Might Not be needed in maintainer
    def check_hash(self, email: str, pwd: str) -> bool:
        """Verifies hashed password with stored hash & verifies maintainer before login

            Args:
                email : Email ID of maintainer
                pwd : Password to be checked
                
            Returns:
                bool
        """
        if value := self.db.maintainer_credentials.find_one(
                {"email": email}
        ):
            dbpwd = value['password']
            salt = dbpwd[:64]
            dbpwd = dbpwd[64:]
            pwd_hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 100000)
            pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
            
            if pwd_hash==dbpwd:
                return True
            else:
                return False
        else:
            return False


    def _approve_contributor(self, contributor: Dict[str, str]):
        """Trigger lambda for contributor addition

        Args:
            contributor (Dict[str, str]): contirbutor details
        """
        project = self.db.project.find_one(
            filter={"_id": contributor["interested_project"]}
        )
        submission = {
            **{"team-slug": project["team_slug"]},
            **{"contributor": contributor["github_id"]},
        }
        response = service.lambda_(func="githubcommunitysrm-v2", payload=submission)

        if response["success"] == False:
            service.sns(
                payload={
                    "message": f"Lambda failing on contirbutor approval contributor_id -> {contributor['_id']} \
                         Error: {response}",
                    "subject": "[LAMBDA-FAILING]",
                }
            )
        else:
            self.db.contributor.find_one_and_update(
                {"_id": contributor["_id"]}, update={"$set": {"is_added_to_repo": True}}
            )

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
            update={"$set": {"is_maintainer_approved": True}},
        )

        if contributor:
            if contributor.get("is_maintainer_approved") and contributor.get(
                "is_admin_approved"
            ):
                raise ContributorApprovedError("Contributor approved")
            Thread(
                target=self._approve_contributor, kwargs={"contributor": contributor}
            ).start()
            project_doc = self.db.project.find_one_and_update(
                {"_id": project_id},
                update={"$addToSet": {"contributor_id": contributor_id}},
            )
            return {**project_doc, **contributor}
        raise ContributorNotFoundError("No contributor found")

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

    def find_contributor_for_removal(
        self, identifier: str, project_ids: list
    ) -> Dict[str, Any]:
        """FInd contributors from contributor id

        Args:
            identifier (str): identifier
            project_ids (list): maintainer project ids

        Returns:
            Dict[str, Any]
        """
        if not len(project_ids):
            raise ProjectErrors("Projects not found")
        contributor = self.db.contributor.find_one_and_delete(
            {
                "_id": identifier,
                "is_admin_approved": True,
                "is_maintainer_approved": False,
                "interested_project": {"$in": project_ids},
            }
        )
        project_name = self.db.project.find_one(
            {"_id": contributor["interested_project"]}
        )["project_name"]

        if contributor:
            contributor["project_name"] = project_name
            return contributor
        raise ContributorNotFoundError("Contributor not found")

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

        if not decode:
            raise AuthenticationErrors("Not allowed to reset")

        if "email" not in decode:
            raise AuthenticationErrors("Email not found invalid JWT")
            
        maintainer = self.db.maintainer_credentials.find_one_and_update(
            {"$and": [{"email": decode.get("email")}, {"reset": True}]},
            update={
                "$set": {
                    "password": self.hash_password(password),
                    "reset": False,
                }
            },
        )

        if maintainer:
            return True
        raise MaintainerNotFoundError("No maintainer found/not allowed to reset")


    def projects_from_email(self, email: str) -> list:
        """Get all projects from email

        Args:
            email (str): maintainer emails

        Returns:
            list: list of all projects
        """
        projects = self.db.maintainer.find(
            {"email": email, "is_admin_approved": True},
            {
                "name": 0,
                "email": 0,
                "srm_email": 0,
                "reg_number": 0,
                "branch": 0,
                "is_admin_approved": 0,
                "time_stamp": 0,
                "github_id": 0,
                "_id": 0,
            },
        )

        projects = list(projects)
        if len(projects):
            return [project["project_id"] for project in projects]
        return False
