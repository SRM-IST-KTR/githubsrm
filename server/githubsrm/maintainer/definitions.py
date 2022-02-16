from typing import Dict, Any
from schema import And, Schema, SchemaError
from core.errorfactory import SchemaError as CustomSchemaError


"""
Module level schema to avoid re-initialization of schema
on every request.
"""

schema = {
    "projects": Schema(
        {
            "contributor_id": And(
                str, lambda contributor_id: len(contributor_id.strip()) == 8
            ),
            "project_id": And(str, lambda project_id: len(project_id.strip()) == 8),
        }
    ),
    "login": Schema(
        {
            "email": And(str, lambda email: len(email.strip()) > 0),
            "password": And(str, lambda password: len(password.strip()) > 0),
        }
    ),
    "reset": Schema({"password": And(str, lambda password: len(password.strip()) > 0)}),
    "set": Schema({"email": And(str, lambda email: len(email.strip()) > 0)}),
    "contributor_rejection": Schema(
        {
            "contributor_id": And(
                str, lambda contirbutor_id: len(contirbutor_id.strip()) == 8
            )
        }
    ),
}


class MaintainerSchema:
    def __init__(self, data: Dict[str, str], path: str) -> None:
        self.data = data
        self.path = path

        self.valid_paths = ["projects", "login", "set", "reset"]

    def valid_schema(self) -> Schema:
        validator = schema[self.path]
        return validator

    def valid(self) -> Dict[str, Dict[str, str]]:
        if self.path not in self.valid_paths:
            return {"error": "Invalid path"}

        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"invalid data": self.data, "error": str(e)})


class RejectionSchema:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def valid(self) -> Dict[str, str]:
        try:
            return schema["contributor_rejection"].validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"error": str(e)})
