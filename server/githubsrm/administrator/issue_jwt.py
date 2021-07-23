from hashlib import new
import os
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from dotenv import load_dotenv

load_dotenv()


class IssueKey:
    def __init__(self):
        self.signature = os.getenv("SIGNATURE")

    def issue_key(self, payload: Dict[str, Any], expiry: float = 24) -> Dict[str, str]:
        """Issue jwt keys with desired payload 
           Jwt Expiry time is set to 24 hours.

        Args:
            payload (Dict[str, Any]): data give

        Returns:
            Dict[str, str]: Jwt token
        """
        payload = {**payload, **
                   {"exp": datetime.utcnow()+timedelta(hours=expiry)}}
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
            if isinstance(key, (tuple, list)):
                _, token = key
                decoded = jwt.decode(jwt=token, key=self.signature,
                                     options={"require": ["exp"], "verify_signature": True}, algorithms=['HS256'])
                return decoded
        except Exception as e:
            print(e)
            return False

        try:
            decoded = jwt.decode(jwt=key, key=self.signature,
                                 options={"require": ["exp"], "verify_signature": True}, algorithms=['HS256'])

            return decoded
        except Exception as e:
            return False

    def verify_role(self, key: str, path: str) -> bool:
        """Verify user permissions

        Args:
            key (str): jwt key passed
            path (str): verify if jwt is allowed on this path

        Returns:
            bool: is allowed
        """
        decoded = jwt.decode(jwt=key, key=self.signature,
                             options={"verify_signature": True}, algorithms=["HS256"])
        if 'admin' in path:
            return decoded.get("admin") == True
        if "maintainer" in path:
            return decoded.get("admin") == None

    def update_key(self, payload: Dict[str, Any], old_token: str) -> str:
        """update jwt with new payload

        Args:
            payload (Dict[str, Any]): payload to be added to jwt
            old_token (str): old jwt token

        Returns:
            str: jwt
        """
        old_jwt = self.verify_key(old_token)
        if old_jwt:
            payload = {**old_jwt, **payload}
            new_key = self.issue_key(payload=payload)
            if new_key:
                return new_key
        else:
            return False
