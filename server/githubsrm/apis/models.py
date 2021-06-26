
from typing import Any, Dict, List
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
import pymongo
from bson import json_util


load_dotenv()


class Entry:

    def __init__(self):
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        self.db = client[os.getenv('MONGO_DB')]

    def _enter_project(self, doc: Dict[str, str], maintainer_id: ObjectId) -> None:
        """Project Entry (only accessed by maintainer)

        Args:
            doc (Dict[str, str]): post to be entred
            maintainer_id (ObjectId): maintainer id 
        """
        doc = {**doc, **maintainer_id}
        self.db.project.insert_one(doc)

    def _update_project(self, identifier: ObjectId,
                        project_id: ObjectId) -> None:
        """Update contributers of the project (only accessed by contributor)

        Args:
            identifier (ObjectId): Contributor ID
            project_id: (ObjectId): Project to add contributors to
        """

        # Check if project exists
        one = self.db.project.find_one({"_id": project_id})

        if one:
            try:
                # Check if contributor exists
                one["contributor_id"]
                self.db.project.update_one({"_id": project_id}, {
                    "$push": {"contributor_id": identifier}})
                return True
            except Exception as e:
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
        try:
            project_url = doc.pop("project_url")
        except Exception as e:
            project_url = None
        poa = doc.pop("poa")

        _id = ObjectId()
        doc = {**doc, **{"_id": _id}}

        try:
            self.db.maintainer.insert_one(doc)

            # Default approve to false
            self._enter_project({
                "project_url": project_url,
                "poa": poa,
                "approved": False
            }, maintainer_id={
                "maintainer_id": _id
            })

            return True

        except Exception as e:
            print(e)
            return False

    def enter_contributor(self, doc: Dict[str, Any]) -> None:
        """Addition of contributors for avaliable Projects

        Args:
            doc (Dict[str, Any])
        """

        _id = ObjectId()
        doc = {**doc, **{"_id": _id}, **{"approved": False}}

        try:
            project_id = ObjectId(doc['interested_project'])
        except Exception as e:
            return

        if len(list(self.db.project.find({"_id": project_id}))) == 0:
            return

        try:
            self.db.contributor.insert_one(doc)
            return True

        except Exception as e:
            print(e)

    def approve_project(self, identifier: ObjectId) -> bool:
        """Approve maintainers

        Args:
            identifier (ObjectId): Project ID

        Returns:
            bool
        """
        try:
            identifier = ObjectId(identifier)
        except Exception as e:
            return

        project = self.db.project.find({"_id": identifier})

        if project:
            self.db.project.update_one({"_id": identifier}, {
                "$set": {"approved": True}})
            return True
        return

    def approve_contributor(self, identifier: ObjectId, project_id: ObjectId) -> bool:
        """Approve contributors to projects

        Returns:
            bool
            identifier: Contributor ID
            project_id: Project ID
        """
        try:
            identifier = ObjectId(identifier)
            project_id = ObjectId(project_id)

        except Exception as e:
            return

        if self._update_project(identifier=identifier, project_id=project_id):
            print("IN")
            self.db.contributor.update({"_id": identifier}, {
                "$set": {"approved": True}})
            return True
        return

    def get_projects(self) -> object:
        """Get all projects

        Returns:
            object: MongoDB cursor
        """
        return self.db.project.find({})

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

    def check_existing(self, poa: str) -> bool:
        result = list(self.db.project.find({"poa": poa}))
        if len(result) != 0:
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
