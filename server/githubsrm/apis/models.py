
from typing import Any, Dict, List
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
import pymongo

load_dotenv()


class Entry:

    def __init__(self):
        client = pymongo.MongoClient(os.getenv('mongo_uri'), port=27017)
        self.db = client[os.getenv('mongo_db')]

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
        #TODO: Set -> Push
        self.db.project.update_one({"_id": project_id}, {
                                   "$set": {"contributor_id": identifier}})

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

            self._enter_project({
                "project_url": project_url,
                "poa": poa
            }, maintainer_id={
                "maintainer_id": _id
            })

            return True

        except Exception as e:
            print(e)
            return False

    # TODO: Fix contributor update in project collection
    def enter_contributor(self, doc: Dict[str, Any]) -> None:
        """Addition of contributors for avaliable Projects

        Args:
            doc (Dict[str, Any])
        """

        project_id = doc['interested_project']
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            print(e)
            return

        _id = ObjectId()
        doc = {**doc, **{"_id": _id}}
        try:

            self.db.contributor.insert_one(doc)
            self._update_project(_id, project_id)
            return True

        except Exception as e:
            print(e)

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

    entry.enter_contributor(
        {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "60d5025ddd176dddd9f89405"
        }
    )
