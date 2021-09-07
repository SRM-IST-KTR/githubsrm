import re
from typing import Any, Dict

from schema import And, Schema, SchemaError
from apis.definitions import check_repo


class AdminSchema:
    def __init__(self, data: Dict[str, str]) -> None:

        self.data = data

        self.email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        self.admin_schema = Schema(
            schema={
                "email": And(str, lambda email: self.email_re.fullmatch(email)),
                "password": str,
            }
        )

    def valid(self) -> Dict[str, str]:
        """Checks for valid data

        Returns:
            Dict[str, str]: data
        """
        try:
            return self.admin_schema.validate(self.data)
        except SchemaError as e:
            return {"invalid_data": self.data, "error": str(e)}


class ApprovalSchema:
    def __init__(self, data: Dict[str, Any], params: str) -> None:
        self.data = data
        self.valid_queries = ["maintainer", "contributor", "project"]
        self.params = params

        self.common = {
            "project_id": And(str, lambda project_id: len(project_id.strip()) == 8)
        }

    def maintainer_valid_schema(self) -> Schema:
        """Returns expected schema for maintainer approval

        Returns:
            Schema
        """

        validator = Schema(
            schema={
                **self.common,
                **{
                    "maintainer_id": And(
                        str, lambda maintainer_id: len(maintainer_id.strip()) == 8
                    ),
                    "email": And(str, lambda email: len(email.strip()) > 0),
                },
            }
        )

        return validator

    def contributor_valid_schema(self) -> Schema:
        """Returns expected schema for contributor approval

        Returns:
            Schema
        """

        validator = Schema(
            schema={
                **self.common,
                **{
                    "contributor_id": And(
                        str, lambda contributor_id: len(contributor_id.strip()) == 8
                    )
                },
            }
        )
        return validator

    def project_valid_schema(self) -> Schema:
        """Returns expected schema for project approval

        Returns:
            Schema
        """
        validator = Schema(
            schema={
                **self.common,
                **{"year": And(str, lambda string: len(string.strip()) == 4)},
            }
        )

        return validator

    def valid(self) -> Dict[str, str]:
        """Checks for valid schema

        Returns:
            Dict[str, str]
        """
        if self.params not in self.valid_queries:
            return {"error": "Invalid query parameters"}
        elif self.params == self.valid_queries[0]:
            try:
                return self.maintainer_valid_schema().validate(self.data)
            except SchemaError as e:
                return {"invalid data": self.data, "error": str(e)}

        elif self.params == self.valid_queries[1]:
            try:
                return self.contributor_valid_schema().validate(self.data)
            except SchemaError as e:
                return {"invalid data": self.data, "error": str(e)}

        else:
            try:
                return self.project_valid_schema().validate(self.data)
            except SchemaError as e:
                return {"invalid data": self.data, "error": str(e)}


class RejectionSchema:
    def __init__(self, data: Dict[str, Any], params: str) -> None:
        """Class for deletion schema

        Args:
            data (Dict[str, Any]): incoming request data
            params (str): query params
        """
        self.data = data
        self.params = params
        self.allowed_params = ["contributor", "maintainer"]

        self.contributor_valid_schema = Schema(
            schema={
                "contributor_id": And(str, lambda contrib: len(contrib.strip()) == 8),
            }
        )

        self.maintainer_valid_schema = Schema(
            schema={
                "maintainer_id": And(
                    str, lambda maintainer_id: len(maintainer_id.strip()) == 8
                )
            }
        )

    def valid(self) -> Dict[str, str]:
        """Get valid remove schema

        Returns:
            Dict[str, str]: schema validation
        """
        if self.params not in self.allowed_params:
            return {"error": "invalid query params"}

        if self.params == "maintainer":
            try:
                return self.maintainer_valid_schema.validate(self.data)
            except SchemaError as e:
                return {"error": str(e)}

        if self.params == "contributor":
            try:
                return self.contributor_valid_schema.validate(self.data)
            except SchemaError as e:
                return {"error": str(e)}
