import re
from typing import Any, Dict

from core.errorfactory import SchemaError as CustomSchemaError
from schema import And, Schema, SchemaError

from .utils import verify_github_details

"""
Module level schema to avoid re-initialization of schema
on every request.
"""

email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

common = {
    "name": And(str, lambda name: len(name.strip()) > 0),
    "email": And(str, lambda email: email_re.fullmatch(email)),
    "srm_email": And(str, lambda email: email.endswith("@srmist.edu.in")),
    "reg_number": And(str, lambda reg: len(reg.strip()) > 0),
    "branch": And(str, lambda branch: len(branch.strip()) > 0),
    "github_id": And(
        str,
        lambda github_id: verify_github_details(
            verify_user=True,
            user_id=github_id,
        ),
    ),
}

schema = {
    "common_schema": {
        "alpha": Schema(
            {
                **common,
                **{
                    "project_name": And(
                        str, lambda project_name: len(project_name.strip()) > 0
                    ),
                    "project_url": And(
                        str,
                        lambda url,: True
                        if not len(url)
                        else verify_github_details(url=url),
                    ),
                    "description": And(
                        str, lambda description: len(description.strip()) >= 30
                    ),
                    "tags": And(
                        list,
                        lambda tags: 2
                        <= len([tag for tag in tags if len(tag.strip())])
                        <= 4,
                    ),
                    "private": bool,
                },
            }
        ),
        "beta": Schema({**common, **{"project_id": And(str, lambda id: len(id) == 8)}}),
        "contributor": Schema(
            {
                **common,
                **{
                    "interested_project": And(
                        str, lambda project_id: len(project_id) == 8
                    ),
                    "poa": And(str, lambda poa: len(poa.strip()) >= 30),
                },
            }
        ),
    },
    "contact_us": Schema(
        {
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email: len(email.strip()) > 0),
            "message": And(str, lambda message: len(message.strip()) > 30),
            "phone_number": And(
                str,
                lambda phone: re.compile("[0-9]{10}").fullmatch(phone)
                if phone
                else True,
            ),
        }
    ),
}


class CommonSchema:
    def __init__(self, data: Dict[Any, Any], query_param: str) -> None:
        self.data = data
        self.query_params = query_param
        self.valid_params = ["contributor", "alpha", "beta"]

    def valid_schema(self) -> Schema:
        validator = schema["common_schema"][self.query_params]
        return validator

    def valid(self) -> Dict[str, Any]:
        if self.query_params not in self.valid_params:
            return {"error": "invalid role"}

        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"invalid data": self.data, "error": str(e)})


class ContactUsSchema:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def valid_schema(self) -> Schema:
        validator = schema["contact_us"]
        return validator

    def valid(self) -> Dict[str, Any]:
        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            raise CustomSchemaError(detail={"invalid data": self.data, "error": str(e)})
