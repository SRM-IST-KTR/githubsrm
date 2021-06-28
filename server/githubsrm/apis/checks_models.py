import pymongo
from django.conf import settings


class EntryCheck:
    def __init__(self) -> None:
        client = pymongo.MongoClient(settings.DATABASE['mongo_uri'])
        self.db = client[settings.DATABASE['db']]

    def check_existing(self, description: str, project_name: str) -> bool:
        """Checks existing project proposals

        Args:
            description (str)
            project_name (str)

        Returns:
            bool: 
        """

        result = list(self.db.project.find({"$or": [
            {"project_name": project_name},
            {"description": description}
        ]}))

        if len(result) > 0:
            return True

        return

    def check_approved_project(self, identifier: str) -> bool:
        """Checks if given identifier is valid and approved status

        Args:
            identifier (str): project_id

        Returns:
            bool
        """
        result = self.db.project.find_one({"_id": identifier})

        if result:
            return result['approved']
        return

    def check_existing_contributor(self, interested_project: str,
                                   reg_number: str) -> bool:
        """Existing contributor to same project

        Args:
            interested_project (str): Project ID
            reg_number (str): Contributor Registration Number

        Returns:
            bool
        """

        result = list(self.db.contributor.find({"$or": [
            {"interested_project": interested_project},
            {"reg_number": reg_number}
        ]}))

        if len(result) > 0:
            return True

        return

    def check_existing_beta(self, github_id: str, project_id: str) -> bool:
        """Checks for existing beta maintainer

        Args:
            github_id (str): beta github ID
            project_id (str): project ID 
        Returns:
            bool
        """

        result = list(self.db.maintainer.find(
            {"github_id": github_id, "project_id": project_id}))

        if len(result) > 1:
            return True

        return
