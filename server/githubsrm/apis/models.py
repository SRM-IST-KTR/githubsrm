from typing import Any, Dict

from core.models import BaseModel

from .errors import MiscErrors, ProjectErrors


class Entry(BaseModel):
    def _enter_project(
        self, doc: Dict[str, str], visibility: bool, project_id: str
    ) -> None:
        """Project Entry (only accessed by maintainer)

        Args:
            doc (Dict[str, str]): post to be entred
            project_id (str): project id
        """

        doc = {**doc, **{"_id": project_id}, **{"private": visibility}}
        self.db.project.insert_one(doc)

    def _update_project(self, identifier: str, project_id: str) -> None:
        """Update contributers of the project (only accessed by contributor)

        Args:
            identifier (str): Contributor ID
            project_id: (str): Project to add contributors to
        """
        project = self.db.project.find_one_and_update(
            {"_id": project_id},
            {"$push": {"contributor_id": identifier}},
            upsert=False,
        )
        if project:
            return True

    def enter_maintainer(self, doc: Dict[str, str]) -> Any:
        """Enter Maintainers

        Args:
            doc (Dict[str, str]): Maintainer Schema
        """
        project_url = doc.get("project_url")

        description = doc.pop("description")
        tags = doc.pop("tags")
        project_name = doc.pop("project_name")

        project_id = self.get_uid()
        _id = self.get_uid()
        doc = {
            **doc,
            **{"_id": _id},
            **{"project_id": project_id},
            **{"is_admin_approved": False},
        }
        existing_maintainer = self.db.maintainer.find_one(
            {"srm_email": doc.get("srm_email"), "reg_number": doc.get("reg_number")}
        )

        if existing_maintainer and "password" in existing_maintainer:
            self.db.maintainer.insert_one(
                {**doc, **{"password": existing_maintainer.get("password")}}
            )

        else:
            self.db.maintainer.insert_one(doc)

        # Default approve to false
        self._enter_project(
            {
                "project_url": project_url,
                "description": description,
                "tags": tags,
                "is_admin_approved": False,
                "project_name": project_name,
                "project_url": project_url,
            },
            visibility=doc["private"],
            project_id=project_id,
        )

        return project_id, _id, project_name, description

    def enter_beta_maintainer(self, doc: Dict[str, Any]) -> str:
        """Add beta maintainers to project and updates maintainers
        collection.
        """
        _id = self.get_uid()

        existing_maintainer = self.db.maintainer.find_one(
            {"srm_email": doc.get("srm_email"), "reg_number": doc.get("reg_number")}
        )

        if existing_maintainer and "password" in existing_maintainer:
            self.db.maintainer.insert_one(
                {
                    **doc,
                    **{"_id": _id},
                    **{"project_id": doc.get("project_id")},
                    **{"is_admin_approved": False},
                    **{"password": existing_maintainer.get("password")},
                }
            )
            return _id

        else:
            self.db.maintainer.insert_one(
                {
                    **doc,
                    **{"_id": _id},
                    **{"project_id": doc.get("project_id")},
                    **{"is_admin_approved": False},
                }
            )
            return _id

    def enter_contributor(self, doc: Dict[str, Any]) -> Dict[str, str]:
        """Addition of contributors for avaliable Projects

        Args:
            doc (Dict[str, Any])
        """

        _id = self.get_uid()
        doc = {
            **doc,
            **{"_id": _id},
            **{"is_admin_approved": False},
            **{"is_maintainer_approved": False},
            **{"is_added_to_repo": False},
        }

        project_doc = self.db.project.find_one({"_id": doc.get("interested_project")})
        if not project_doc:
            raise ProjectErrors(
                detail={"error": "Project not approved or project does not exist"}
            )

        self.db.contributor.insert_one(doc)
        return {**doc, **project_doc}

    def beta_maintainer_reset_status(self, maintainer_id: str) -> None:
        self.db.maintainer.delete_one({"_id": maintainer_id})

    def alpha_maintainer_reset_status(
        self, project_id: str, maintainer_id: str
    ) -> None:
        self.db.project.delete_one({"_id": project_id})
        self.db.maintainer.delete_one({"_id": maintainer_id})

    def delete_contributor(self, identifier: str) -> bool:
        self.db.project.delete_one({"contributor_id": identifier})
        self.db.contributor.delete_one({"_id": identifier})

    def get_projects(self, admin: bool = False) -> object:
        if admin:
            self.db.project.find({})
        return self.db.project.find(
            {"private": False, "is_admin_approved": True},
            {"maintainer_id": 0, "team_slug": 0},
        )

    def get_contributors(self) -> object:
        return self.db.contributor.find({})

    def get_maintainers(self) -> object:
        return self.db.maintainer.find({})

    def get_team_data(self) -> object:
        return self.db.team.find({})

    def enter_contact_us(self, doc: Dict[str, Any]) -> bool:
        details = self.db.contactUs.find_one({"message": doc.get("message")})

        if details:
            raise MiscErrors(
                status_code=409, detail={"error": "Message already exists!"}
            )
        self.db.contactUs.insert_one(doc)

    def get_contact_us(self) -> object:
        return self.db.contactus.find({})

    def get_project_from_id(self, identifier: str) -> Dict[str, Any]:
        project = self.db.project.find_one({"_id": identifier})
        if project:
            return project

        return None
