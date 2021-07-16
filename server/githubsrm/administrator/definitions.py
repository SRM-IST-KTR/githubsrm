
import re
from typing import Any, Dict

from schema import And, Schema, SchemaError
from apis.definitions import check_repo


class AdminSchema:
    def __init__(self, data: Dict[str, str]) -> None:

        self.data = data

        self.email_re = re.compile(
            '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        self.admin_schema = Schema(
            schema={
                "email": And(str, lambda email: self.email_re.fullmatch(email)),
                "password": str
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
            return {
                "invalid_data": self.data,
                "error": str(e)
            }


class ApprovalSchema:
    def __init__(self, data: Dict[str, Any], params: str) -> None:
        self.data = data
        self.valid_queries = ['maintainer', 'contributor', 'project']
        self.params = params

        self.common = {
            "project_id": And(str, lambda project_id: len(project_id.strip()) == 8)
        }

    def maintainer_valid_schema(self) -> Schema:
        """Returns expected schema for maintainer approval

        Returns:
            Schema
        """

        validator = Schema(schema={**self.common, **{
            "maintainer_id": And(str, lambda maintainer_id: len(maintainer_id.strip()) == 8),
            "email": And(str, lambda email: len(email.strip()) > 0))
        }})

        return validator

    def contributor_valid_schema(self) -> Schema:
        """Returns expected schema for contributor approval

        Returns:
            Schema
        """

        validator = Schema(schema={**self.common, **{
            "contributor_id": And(str, lambda contributor_id: len(contributor_id.strip()) == 8)
        }})
        return validator

    def project_valid_schema(self) -> Schema:
        """Returns expected schema for project approval

        Returns:
            Schema
        """
        validator = Schema(schema={**self.common, **{
            "private": bool,
            "project_url": And(str, lambda project_url: check_repo(project_url))
        }})

        return validator

    def valid(self) -> Dict[str, str]:
        """Checks for valid schema

        Returns:
            Dict[str, str]
        """
        if self.params not in self.valid_queries:
            return {
                "error": "Invalid query parameters"
            }
        elif self.params == self.valid_queries[0]:
            try:
                return self.maintainer_valid_schema().validate(self.data)
            except SchemaError as e:
                return {
                    "invalid data": self.data,
                    "error": str(e)
                }

        elif self.params == self.valid_queries[1]:
            try:
                return self.contributor_valid_schema().validate(self.data)
            except SchemaError as e:
                return {
                    "invalid data": self.data,
                    "error": str(e)
                }

        else:
            try:
                return self.project_valid_schema().validate(self.data)
            except SchemaError as e:
                return {
                    "invalid data": self.data,
                    "error": str(e)
                }
