from requests.api import request
from schema import Schema, And, SchemaError
from typing import Any, Callable, Dict
import re
import requests
import cProfile

session = requests.Session()

def get_json_schema(id: int, valid_schema: Callable) -> dict:
    """Generate json schema

    Args:
        id (int)

    Returns:
        dict
    """
    validator = valid_schema()
    return validator.json_schema(schema_id=id)


def check_github_id(github_id: str):
    """Checks GitHub ID

    Args:
        github_id (str) user entred value
    """
    if len(github_id.strip()):
        _url = f"https://github.com/{github_id}"

        response = session.get(_url)

        return response.status_code == 200
    return False


def check_repo(url: str):
    """Check github repo

    Args:
        url (str): [description]
    """
    if len(url) == 0:
        return True

    response = session.get(url)
    return response.status_code == 200


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


def check_poa(poa: str) -> bool:
    """Checks valid poa

    Args:
        poa (str)

    Returns:
        bool
    """
    return len(poa.strip()) >= 30


def check_phone(ph: str) -> bool:
    """Check correct phone number

    Args:
        ph (str)

    Returns:
        bool
    """
    if len(ph) == 0:
        return True

    phone_re = re.compile("[0-9]{10}")
    return phone_re.fullmatch(ph)


class CommonSchema:
    def __init__(self, data: Dict[Any, Any], query_param: str) -> None:
        self.data = data
        self.email_re = re.compile(
            '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        self.url_re = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

        self.query_params = query_param
        self.common = {
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email: self.email_re.fullmatch(email)),
            "srm_email": And(str, lambda email: email.endswith('@srmist.edu.in')),
            "reg_number": And(str, lambda reg: len(reg.strip()) > 0),
            "branch": And(str, lambda branch: len(branch.strip()) > 0),
            "github_id": And(str, lambda github_id: check_github_id(github_id=github_id))
        }

        self.alpha_maintainer = {
            "project_name": And(str, lambda project_name: len(project_name.strip()) > 0),
            "project_url": And(str, lambda url: check_repo(url)),
            "description": And(str, lambda description: len(description.strip()) >= 30),
            "tags": And(list, lambda tags: check_tags(tags=tags))
        }

        self.beta_maintainer = {
            "project_id": And(str, lambda id: len(id) == 8)
        }

        self.contributor = {
            "interested_project": And(str, lambda project_id: len(project_id) == 8),
            "poa": And(str, lambda poa: check_poa(poa))
        }

    @staticmethod
    def check_path(query_param: str) -> str:
        """Checks query param

        Args:
            query_param (str)

        Returns:
            str
        """
        if 'contributor' in query_param:
            return 'contributor'
        elif 'alpha' in query_param:
            return 'alpha'
        elif 'beta' in query_param:
            return 'beta'
        else:
            return

    def valid_schema(self) -> Schema:
        direction = self.check_path(self.query_params)

        if direction == 'contributor':
            validator = Schema(schema={**self.common, **self.contributor})
            return validator
        elif direction == 'alpha':
            validator = Schema(schema={**self.common, **self.alpha_maintainer})
            return validator
        elif direction == 'beta':
            validator = Schema(schema={**self.common, **self.beta_maintainer})
            return validator
        else:
            return

    def get_json(self, id: int) -> dict:
        """Generate schema

        Args:
            id (int)

        Returns:
            dict
        """
        return get_json_schema(id=id, valid_schema=self.valid_schema)

    def valid(self) -> Dict[str, Any]:
        """Checks schema

        Returns:
            Dict[str, Any]: [description]
        """
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

    def valid_schema(self) -> Schema:
        """Generate valid schema for contact us route

        Returns:
            Schema
        """
        validator = Schema(schema={
            "name": And(str, lambda name: len(name.strip()) > 0),
            "email": And(str, lambda email: len(email.strip()) > 0),
            "message": And(str, lambda message: len(message.strip()) > 30),
            "phone_number": And(str, lambda phone: check_phone(phone))
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

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        validate = CommonSchema(data={
            "name": "Aradhya",
            "github_id": "Aradhya-Tripathi",
            "description": "This is a random description for a tester project",
            "reg_number": "RA1911004010187",
            "srm_email": "at8029@srmist.edu.in",
            "email": "aradhyatripathi51@gmail.com",
            "project_url": "https://github.com/Aradhya-Tripathi",
            "tags": ["django", "nextjs"],
            "branch": "ECE",
            "project_name": "Random Project"
        }, query_param="alpha").valid()

    print(pr.print_stats())

    print(validate)