import os
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from dotenv import load_dotenv

load_dotenv()


class IssueKey:
    def __init__(self):
        self.signature = os.getenv("SIGNATURE")

    def issue_key(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """Issue jwt keys with desired payload 
           Jwt Expiry time is set to 24 hours.

        Args:
            payload (Dict[str, Any]): data give

        Returns:
            Dict[str, str]: Jwt token
        """
        payload = {**payload, **{"exp": datetime.utcnow()+timedelta(hours=24)}}
        try:
            return jwt.encode(
                payload=payload, key=self.signature
            )
        except Exception as e:
            return False

    def verify_key(self, key: str) -> bool:
        """Verify JwT with the original signature

        Args:
            key (str): jwt key

        Returns:
            bool
        """

        try:
            jwt.decode(jwt=key, key=self.signature,
                       options={"require": ["exp"], "verify_signature": True}, algorithms=['HS256'])

            return True
        except Exception as e:
            return False


if __name__ == '__main__':
    # from administrator import entry, issue_key
    # print(issue_key.issue_key())

    issue = IssueKey()
    key = issue.issue_key(payload={
        "name": "someone",
        "is_admin": True
    })

    print(issue.verify_key(key=key))
