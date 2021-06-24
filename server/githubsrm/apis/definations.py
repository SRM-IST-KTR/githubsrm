from schema import Optional, Schema, And, SchemaError
from typing import Any, Dict
import re
from django.http.request import HttpHeaders


class CommonSchema:
    def __init__(self, data: Dict[Any, Any], headers: HttpHeaders) -> None:
        self.data = data
        self.email_re = re.compile(
            '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        self.url_re = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')

        self.headers = headers
        self.common = {
            "name": str,
            "email": And(str, lambda email:  self.email_re.fullmatch(email)),
            "srm_email": str,
            "reg_number": And(str, lambda reg: len(reg) == 15),
            "branch": str,
            "github_id": str,
        }

        self.maintainer = {
            Optional("project_url"): And(str, lambda url: self.url_re.fullmatch(url)),
            "poa": str
        }

        self.contributor = {
            "interested_project": str,
            Optional("feature", default=None): str
        }

    def valid_schema(self) -> Schema:

        if self.check_path(self.headers.get('path_info')) == 'contrib':
            validator = Schema(schema=self.merge(
                self.common, self.contributor))
            return validator

        validator = Schema(schema=self.merge(self.common, self.maintainer))
        return validator

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
            "name": str,
            "github_id": str,
            "linkedin": And(str, lambda url: self.url_re.fullmatch(url)),
            Optional("twitter", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            Optional("portfolio", default=None): And(str, lambda url: self.url_re.fullmatch(url)),
            "img_url": And(str, lambda url: self.url_re.fullmatch(url)),
            "tagline": str
        })

        return valdiator

    def valid(self) -> Dict[str, Any]:
        try:
            return self.valid_schema().validate(self.data)
        except SchemaError as e:
            return {
                "invalid data": self.data,
                "error": str(e)
            }
