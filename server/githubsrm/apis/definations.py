from bson.json_util import default
from schema import Optional, Schema, And, SchemaError
from typing import Any, Callable, Dict
import re
from django.http.request import HttpHeaders
import json


def get_json_schema(id: int, valid_schema: Callable) -> dict:
    """Generate json schema

    Args:
        id (int)

    Returns:
        dict
    """
    validator = valid_schema()
    return validator.json_schema(schema_id=id)


def check_github_id(github_ids: list) -> bool:
    """Check valid GitHub IDs

    Args:
        github_ids (list)

    Returns:
        bool
    """

    if len(github_ids):
        pass
    else:
        return False

    for ids in github_ids:
        if len(ids.strip()) == 0:
            return False

    return True


class CommonSchema:
    def __init__(self, data: Dict[Any, Any], headers: HttpHeaders) -> None:
        self.data = data
        self.email_re = re.compile(
            '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        self.url_re = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

        self.reg_number = re.compile("^RA[0-9]{13}$")

        self.headers = headers
        self.common = {
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email:  self.email_re.fullmatch(email)),
            "srm_email": And(str, lambda email: email.endswith('@srmist.edu.in')),
            "reg_number": And(str, lambda reg: self.reg_number.fullmatch(reg)),
            "branch": And(str, lambda branch: len(branch.strip()) > 0)
        }

        self.maintainer = {
            "github_id": And(list, lambda github_ids: check_github_id(github_ids)),
            Optional("project_url", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            "poa": And(str, lambda poa: len(poa.strip()) > 0)
        }

        self.contributor = {
            "github_id": And(str, lambda github_id: len(github_id.strip()) > 0),
            "interested_project": And(str, lambda name: len(name.strip()) > 0),
            Optional("feature", default=None): And(str, lambda feature: len(feature.strip()) > 0)
        }

    def valid_schema(self) -> Schema:

        if self.check_path(self.headers.get('path_info')) == 'contrib':
            validator = Schema(schema=self.merge(
                self.common, self.contributor))
            return validator

        validator = Schema(schema=self.merge(self.common, self.maintainer))
        return validator

    def get_json(self, id: int) -> dict:
        """Generate schema

        Args:
            id (int)

        Returns:
            dict
        """
        return get_json_schema(id=id, valid_schema=self.valid_schema)

    def check_path(self, path_info: str) -> str:
        if 'contributor' in path_info:
            return 'contrib'
        return 'maintainer'

    @staticmethod
    def merge(schema_1: Dict[str, Any], schema_2: Dict[str, Any]):
        schema_1.update(schema_2)
        return schema_1

    def valid(self) -> Dict[str, Any]:
        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            return {
                "invalid data": self.data,
                "error": str(e)
            }


class TeamSchema:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self.data = data
        self.url_re = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

    def valid_schema(self) -> Schema:
        valdiator = Schema(schema={
            "name": And(str, lambda name: len(name) > 0),
            "github_id": And(str, lambda github_id: len(github_id) > 0),
            "linkedin": And(str, lambda url: self.url_re.fullmatch(url)),
            Optional("twitter", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            Optional("portfolio", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            "img_url": And(str, lambda url: self.url_re.fullmatch(url)),
            "tagline": And(str, lambda tagline: len(tagline) > 0)
        })

        return valdiator

    def get_json(self, id: int) -> dict:
        """Generate schema

        Args:
            id (int)

        Returns:
            dict
        """
        return get_json_schema(id=id, valid_schema=self.valid_schema)

    def valid(self) -> Dict[str, Any]:
        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            return {
                "invalid data": self.data,
                "error": str(e)
            }


if __name__ == '__main__':
    schema = CommonSchema(data={

        "name": "Aradhya",
        "email": "testuser@localhost.com",
        "srm_email": "tu6969@srmist.edu.in",
        "reg_number": "RA1911004010187",
        "branch": "ECE",
        "github_id": ["Test-User"],
        "poa": "TestProject"

    }, headers={"path_info": "apis/maintainer"})

    print(json.dumps(schema.get_json(id=1), indent=4))

    schema = CommonSchema(data={

        "name": "Aradhya",
        "email": "testuser@localhost.com",
        "srm_email": "tu6969@srmist.edu.in",
        "reg_number": "RA1911004010187",
        "branch": "ECE",
        "github_id": "Test-User",
        "interested_project": "60d59693278a6b1bbe4fa9df"

    }, headers={"path_info": "apis/contributor"})

    # print(json.dumps(schema.get_json(id=2), indent=4))
