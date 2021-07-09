
import re
from typing import Dict

from schema import And, Schema, SchemaError

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
