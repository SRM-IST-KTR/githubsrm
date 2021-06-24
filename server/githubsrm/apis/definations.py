from schema import Optional, Schema, And, SchemaError
from typing import Any, Dict, List
import re


class CommonSchema:
    def __init__(self, data: Dict[Any, Any]) -> None:
        self.data = data
        self.email_re = re.compile(
            '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')

    def valid_schema(self) -> Schema:
        validator = Schema(schema={
            "name": str,
            "email": And(str, lambda email:  self.email_re.fullmatch(email)),
            "srm_email": str,
            "reg_number": And(str, lambda reg: len(reg) == 15),
            "branch": str,
            "github_id": str,
            "interested_project": str,
            Optional("feature", default=None): str
        })

        return validator

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
