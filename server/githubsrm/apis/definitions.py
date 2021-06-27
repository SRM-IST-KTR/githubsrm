
from schema import Optional, Schema, And, SchemaError
from typing import Any, Callable, Dict
import re
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


def check_tags(tags: list) -> bool:
    """Checks available tags 

    Args:
        tags

    Returns:
        bool
    """

    for tag in tags:
        if len(tag.strip()) == 0:
            return False

    return len(tags) >= 2 and len(tags) <= 4


class CommonSchema:
    def __init__(self, data: Dict[Any, Any], headers: Dict[str, str]) -> None:
        self.data = data
        self.email_re = re.compile(
            '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        self.url_re = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

        self.headers = headers
        self.common = {
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email:  self.email_re.fullmatch(email)),
            "srm_email": And(str, lambda email: email.endswith('@srmist.edu.in')),
            "reg_number": And(str, lambda reg: len(reg.strip()) > 0),
            "branch": And(str, lambda branch: len(branch.strip()) > 0)
        }

        self.maintainer = {
            "project_name": And(str, lambda project_name: len(project_name.strip()) > 0),
            "github_id": And(list, lambda github_ids: check_github_id(github_ids)),
            Optional("project_url", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            "description": And(str, lambda description: len(description.strip()) > 30),
            "tags": And(list, lambda tags: check_tags(tags=tags))
        }

        self.contributor = {
            "github_id": And(str, lambda github_id: len(github_id.strip()) > 0),
            "interested_project": And(str, lambda name: len(name.strip()) > 0),
            Optional("poa", default=None): And(str, lambda poa: len(poa.strip()) > 30)

        }

    @staticmethod
    def check_path(path_info: str) -> str:
        if 'contributor' in path_info:
            return 'contrib'
        return 'maintainer'

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


class ContactUsSchema:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self.phone_re = re.compile("[0-9]{10}")

    def valid_schema(self) -> Schema:
        """Generate valid schema for contact us route

        Returns:
            Schema
        """
        validator = Schema(schema={
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email: len(email.strip()) > 0),
            "message": And(str, lambda message: len(message.strip()) > 30),
            Optional("phone_number", default=None): And(str, lambda phone: self.phone_re.fullmatch(phone))
        })

        return validator

    def valid(self) -> Dict[str, Any]:
        """Checks entry

        Returns:
            Dict[str, Any]
        """
        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            return {
                "invalid data": self.data,
                "error": str(e)
            }
