
from typing import Any, Dict
import random
import string
from dotenv import load_dotenv
import pymongo
from django.conf import settings


load_dotenv()


class Entry:

    def __init__(self):
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def get_uid(self) -> str:
        """Returns 8 character alpha numeric unique id

        Args:
            length (int)
            operator (pymongo.MongoClient)

        Returns:
            str
        """

        gen_id = random.choices(string.ascii_uppercase+string.digits, k=8)

        if len(list(self.db.collection.find({"_id": gen_id}))) > 0:
            return self.get_uid(length=8)

        return ''.join(gen_id)

    def _enter_project(self, doc: Dict[str, str], maintainer_id: str,
                       visibility: Dict[str, str]) -> None:
        """Project Entry (only accessed by maintainer)

        Args:
            doc (Dict[str, str]): post to be entred
            maintainer_id (str): maintainer id 
        """
        _id = self.get_uid()
        doc = {**doc, **maintainer_id, **{"_id": _id}, **visibility}
        self.db.project.insert_one(doc)

    def _update_project(self, identifier: str,
                        project_id: str) -> None:
        """Update contributers of the project (only accessed by contributor)

        Args:
            identifier (str): Contributor ID
            project_id: (str): Project to add contributors to
        """

        # Check if project exists
        project = self.db.project.find_one({"_id": project_id})
        if project:
            # Check if contributors exists
            if "contributor_id" in project:
                self.db.project.update_one({"_id": project_id}, {
                    "$push": {"contributor_id": identifier}})
                return True
            else:
                # Creates new contributor if no contributor present
                self.db.project.update_one({"_id": project_id}, {"$set": {
                    "contributor_id": [identifier]
                }})

                return True
        return

    def enter_maintainer(self, doc: Dict[str, str]) -> Any:
        """Enter Maintainers

        Args:
            doc (Dict[str, str]): Maintainer Schema

        Returns:
            Any
        """
        project_url = doc.pop("project_url")

        poa = doc.pop("poa")
        tags = doc.pop("tags")
        project_name = doc.pop('project_name')

        _id = self.get_uid()
        doc = {**doc, **{"_id": _id}}

        try:
            self.db.maintainer.insert_one(doc)
            if project_url:
                visibility = {"private": False}
            else:
                visibility = {"private": True}
            # Default approve to false
            self._enter_project({
                "project_url": project_url,
                "poa": poa,
                "tags": tags,
                "approved": False,
                "project_name": project_name
            }, maintainer_id={
                "maintainer_id": _id
            }, visibility=visibility)

            return True

        except Exception as e:
            print(e)
            return False

    def enter_contributor(self, doc: Dict[str, Any]) -> None:
        """Addition of contributors for avaliable Projects

        Args:
            doc (Dict[str, Any])
        """

        _id = self.get_uid()
        doc = {**doc, **{"_id": _id}, **{"approved": False}}

        try:
            project_id = doc['interested_project']
        except Exception as e:
            return

        if len(list(self.db.project.find({"_id": project_id}))) == 0:
            return

        try:
            self.db.contributor.insert_one(doc)
            return True

        except Exception as e:
            print(e)

    def delete_contributor(self, identifier: str) -> bool:
        """Delete Contributos

        Args:
            identifier (str): Contributor ID

        Returns:
            bool
        """
        try:
            # project_contributor = self.db.project.find({"contributor_id": identifier})
            # if len(list(project_contributor)) > 0:
            self.db.project.delete_one({"contributor_id": identifier})

            self.db.contributor.delete_one({"_id": identifier})
            return True
        except Exception as e:
            return

    def approve_project(self, identifier: str) -> bool:
        """Approve project

        Args:
            identifier (str): Project ID

        Returns:
            bool
        """

        project = self.db.project.find({"_id": identifier})

        if project:
            self.db.project.update_one({"_id": identifier}, {
                "$set": {"approved": True}})
            return True
        return

    def approve_contributor(self, identifier: str, project_id: str) -> bool:
        """Approve contributors to projects

        Returns:
            bool
            identifier: Contributor ID
            project_id: Project ID
        """
        if len(list(self.db.contributor.find({"_id": identifier}))) > 0: 
            if self._update_project(identifier=identifier, project_id=project_id):
                self.db.contributor.update({"_id": identifier}, {
                    "$set": {"approved": True}})
                return True
        return

    def get_projects(self, admin: bool = False) -> object:
        """Get all public projects / all project for admin

        Returns:
            object: MongoDB cursor
            admin (bool): admin access
        """
        if admin:
            self.db.project.find({})
        return self.db.project.find({"private": False, "approved": True})

    def get_contributors(self) -> object:
        """Get all existing contributors

        Returns:
            [type]: MongoDB cursor
        """
        return self.db.contributor.find({})

    def get_maintainers(self) -> object:
        """Get all maintainers and status

        Returns:
            [type]: MongoDB cursor 
        """
        return self.db.maintainer.find({})

    def check_existing(self, poa: str, project_name: str) -> bool:
        result_poa = list(self.db.project.find(
            {"poa": poa}))

        result_project_name = list(
            self.db.project.find({"project_name": project_name}))

        if len(result_poa) != 0 or len(result_project_name) != 0:
            return True
        return

    def get_team_data(self) -> object:
        """Get all team data

        Returns:
            [type]: MongoDB cursor 
        """
        return self.db.team.find({})

    def check_existing_contributor(self, interested_project: str,
                                   reg_number: str) -> bool:
        """Existing contributor to same project

        Args:
            interested_project (str): Project ID
            reg_number (str): Contributor Registration Number

        Returns:
            bool
        """
        contributor = list(self.db.contributor.find({
            "interested_project": interested_project,
            "reg_number": reg_number
        }))

        if len(contributor):
            return True
        return


if __name__ == '__main__':
    entry = Entry()
    entry.enter_maintainer(
        {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User"],
            "poa": "TestProject"
        }
    )

    entry.approve_project(identifier="60d59a80b4dbf235af1e3092")

    entry.enter_contributor(
        {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "60d59693278a6b1bbe4fa9df"
        }
    )

    # entry.approve_contributor(
    #     identifier="60d596b85972c9bfc0ed74a4", project_id="60d59693278a6b1bbe4fa9df")

    for objects in entry.get_projects():
        print(objects)
