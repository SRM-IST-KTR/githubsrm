from typing import Dict, Any
from schema import And, Schema, SchemaError


class MaintainerSchema:
    def __init__(self, data: Dict[str, str], path: str) -> None:
        self.data = data
        self.path = path

    def approve_valid_schema(self) -> Schema:
        """Returns valid schema for accepting contributors

        Returns:
            Schema
        """

        validator = Schema(
            schema={
                "contributor_id": And(
                    str, lambda contributor_id: len(contributor_id.strip()) == 8
                ),
                "project_id": And(str, lambda project_id: len(project_id.strip()) == 8),
            }
        )

        return validator

    def login_valid_schema(self) -> Schema:
        """Returns valid schema for maintainer login

        Returns:
            Schema
        """

        validator = Schema(
            schema={
                "email": And(str, lambda email: len(email.strip()) > 0),
                "password": And(str, lambda password: len(password.strip()) > 0),
            }
        )

        return validator

    def reset_valid_schema(self) -> Schema:
        """Returns valid schema for reset password

        Returns:
            Schema
        """

        validator = Schema(
            schema={"password": And(str, lambda password: len(password.strip()) > 0)}
        )

        return validator

    def set_valid_schema(self) -> Schema:
        """Returns valid schema for set password

        Returns:
            Schema
        """
        validator = Schema(
            schema={"email": And(str, lambda email: len(email.strip()) > 0)}
        )

        return validator

    def valid(self) -> Dict[str, Dict[str, str]]:
        """Checks validity of approval data

        Returns:
            Dict[str, str]
        """

        try:
            if self.path == "/maintainer/projects":
                return self.approve_valid_schema().validate(self.data)
            elif self.path == "/maintainer/login":
                return self.login_valid_schema().validate(self.data)
            elif self.path == "/maintainer/reset-password/set":
                return self.reset_valid_schema().validate(self.data)
            else:
                return self.set_valid_schema().validate(self.data)
        except SchemaError as e:
            return {"invalid data": self.data, "error": str(e)}


class RejectionSchema:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.valid_contributor_schema = {
            "contributor_id": And(
                str, lambda contirbutor_id: len(contirbutor_id.strip()) == 8
            )
        }

    def valid(self) -> Dict[str, str]:
        try:
            return Schema(schema=self.valid_contributor_schema).validate(self.data)
        except SchemaError as e:
            return {"error": str(e)}
