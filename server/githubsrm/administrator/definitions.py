import re
from typing import Any, Dict

from core.errorfactory import SchemaError as CustomSchemaError
from schema import And, Schema, SchemaError


email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


common = {"project_id": And(str, lambda project_id: len(project_id.strip()) == 8)}

schema = {
    "approval": {
        "maintainer": Schema(
            {
                **common,
                **{
                    "maintainer_id": And(
                        str, lambda maintainer_id: len(maintainer_id.strip()) == 8
                    ),
                    "email": And(str, lambda email: len(email.strip()) > 0),
                },
            }
        ),
        "contributor": Schema(
            {
                **common,
                **{
                    "contributor_id": And(
                        str, lambda contributor_id: len(contributor_id.strip()) == 8
                    )
                },
            }
        ),
        "project": Schema(
            {
                **common,
                **{"year": And(str, lambda string: len(string.strip()) == 4)},
            }
        ),
    },
    "rejection": {
        "contributor": Schema(
            schema={
                "contributor_id": And(str, lambda contrib: len(contrib.strip()) == 8),
            }
        ),
        "maintainer": Schema(
            schema={
                "maintainer_id": And(
                    str, lambda maintainer_id: len(maintainer_id.strip()) == 8
                )
            }
        ),
    },
    "admin": Schema(
        {
            "email": And(str, lambda email: email_re.fullmatch(email)),
            "password": str,
        }
    ),
}


class AdminSchema:
    def __init__(self, data: Dict[str, str]) -> None:
        self.data = data

    def valid(self) -> Dict[str, str]:
        try:
            return schema["admin"].validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"invalid_data": self.data, "error": str(e)})


class ApprovalSchema:
    def __init__(self, data: Dict[str, Any], params: str) -> None:
        self.data = data
        self.valid_queries = ["maintainer", "contributor", "project"]
        self.params = params

    def valid(self) -> Dict[str, str]:
        if self.params not in self.valid_queries:
            return {"error": "Invalid query parameters"}
        try:
            return schema["approval"][self.params].validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"error": str(e)})


class RejectionSchema:
    def __init__(self, data: Dict[str, Any], params: str) -> None:
        self.data = data
        self.params = params
        self.allowed_params = ["contributor", "maintainer"]

    def valid(self) -> Dict[str, str]:
        if self.params not in self.allowed_params:
            return {"error": "invalid query params"}
        try:
            return schema["rejection"][self.params].validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"error": str(e)})
