
import secrets
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict
from threading import Thread

import pymongo
from django.conf import settings
from dotenv import load_dotenv
from pymongo import ReturnDocument

from core import service


import hashlib, binascii, os

service = BotoService()

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


    def hash_password(self, pwd: str) -> str:
        """Hashes password using salted password hashing (SHA512 & PBKDF_HMAC2)
            Args:
                pwd : Password to be hashed
                
            Returns:
                str : Hashed password
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        # print("SALT1: ", salt)
        pwd_hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode('ascii')
        # print("FINAL HASHED PWD:", final_hashed_pwd)
        return final_hashed_pwd


    def check_hash(self, email: str, pwd: str) -> bool:
        """Verifies hashed password with stored hash & verifies admin before login

            Args:
                email : Email ID of admin
                pwd : Password to be checked
                
            Returns:
                bool
        """
        if value := self.db.admins.find_one(
                {"email": email}
        ):
            dbpwd = value['password']
            #print("DBPWD: ", dbpwd)

            #PASSWORD HASH AND SALT STORED IN DATABASE
            salt = dbpwd[:64]
            #print("SALT2: ", salt)
            dbpwd = dbpwd[64:]
            #print("Stored password hash: ", dbpwd)
            
            #PASSWORD HASH FOR PASSWORD THAT USER HAS CURRENTLY ENTERED
            pwd_hash = hashlib.pbkdf2_hmac('sha512', pwd.encode('utf-8'), salt.encode('ascii'), 100000)
            pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
            #print("pwd_hash: ", pwd_hash)
            
            if pwd_hash==dbpwd:
                #print("Hash Match")
                return True
            else:
                #print("Hash does NOT match")
                return False

        else:
            #print("User NOT in DB")
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

    def find_maintainer_for_approval(self, maintainer_id: str, project_id: str,
                                     maintainer_email: str) -> bool:
        """find and approve maintainer

        Args:
            maintainer_id (str): maintainer identifier
            project_id (str): project identifier
            maintainer_email (str): maintainer_email 

        Returns:
            bool
        """

        maintainer = self.db.maintainer.find_one_and_update(
            {"_id": maintainer_id, "project_id": project_id,
                "email": maintainer_email},
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

    def get_maintainer_github_id(self, maintainer_ids: list):
        """get github ids from maintainer document

        Args:
            maintainer_ids (list): maintainer id list
        """
        val = []
        if maintainers := list(self.db.maintainer.find(filter={"_id": {"$in": maintainer_ids}})):
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
                project_doc["maintainer_id"])
            submission = {**{"project-name": project_doc["project_name"]}, **{"project-description": project_doc["description"]},
                          **{"year": year}, **{"private": project_doc["private"]}, **{"maintainers": maintainer_github_id}}
            response = service.lambda_(
                func="githubcommunitysrm-v1", payload=submission)

            if response["success"] and project_doc["is_admin_approved"] == False:
                project = self.db.project.find_one_and_update(
                    {"_id": identifier},
                    update={
                        "$set": {
                            "is_admin_approved": True,
                            "year": year,
                            "team_slug": response["team-slug"],
                            "private": response["private"],
                            "project_url": response["repo-link"]
                        }
                    }, return_document=ReturnDocument.BEFORE)
                project = {**project, **{"project_url": response["repo-link"]}}
                return project
            else:
                if response["success"] == False:
                    Thread(target=service.sns, kwargs={"payload": {
                        "message": "Lambda returned success false",
                        "subject": "Lambda failed"
                    }}).start()
                return False
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
                "project_url": "",
                "team_slug": "",
                "year": ""
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

    def admin_remove_maintainer(self, identifier: str) -> bool:
        """Admin remove maintainer

        Args:
            identifier (str): maintainer id

        Returns:
            bool:
        """

        maintainer = self.db.maintainer.find_one_and_delete({
            "_id": identifier,
            "is_admin_approved": False
        })

        if not maintainer:
            return False

        project_id = maintainer["project_id"]

        project_name = self.db.project.find_one(
            {"_id": project_id})["project_name"]

        project = self.db.project.find_one_and_delete({
            "_id": project_id,
            "maintainer_id": {"$exists": False}
        })

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

        contributor = self.db.contributor.find_one_and_delete({
            "_id": identifier,
            "is_maintainer_approved": False,
            "is_admin_approved": False
        })

        if contributor:
            project_name = self.db.project.find_one(
                {"_id": contributor["interested_project"]})["project_name"]
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
