import os
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from dotenv import load_dotenv
from .errors import AuthenticationErrors

load_dotenv()


class IssueKey:
    def __init__(self):
        self.signature = os.getenv("SIGNATURE")

    def issue_key(
        self,
        payload: Dict[str, Any],
        expiry: float = 10,
        get_refresh_token: bool = False,
        refresh_expiry: int = 1,
    ) -> Dict[str, str]:
        """Issue jwt keys with desired payload
           Jwt Expiry time is set to 24 hours.

        Args:
            payload (Dict[str, Any]): data give
            get_refresh_token (bool): generate refresh token

        Returns:
            Dict[str, str]: Jwt token
        """

        generation_time = datetime.utcnow()
        payload = {**payload, **{"exp": generation_time + timedelta(minutes=expiry)}}

        if get_refresh_token:
            email = payload.get("email", payload.get("user"))
            refresh_payload = {
                "exp": generation_time + timedelta(days=refresh_expiry),
                "refresh": True,
            }
            refresh_payload.update(
                {"email": email, "name": payload.get("name", "Anonymous")}
            )

            return {
                "access_token": jwt.encode(payload, key=self.signature),
                "refresh_token": jwt.encode(refresh_payload, key=self.signature),
            }

        return jwt.encode(payload=payload, key=self.signature)

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
                decoded = jwt.decode(
                    jwt=token,
                    key=self.signature,
                    options={"require": ["exp"], "verify_signature": True},
                    algorithms=["HS256"],
                )
                return decoded

            elif isinstance(key, dict):
                access_token, _ = key["access_token"], key["refresh_token"]
                decoded = jwt.decode(
                    jwt=access_token,
                    key=self.signature,
                    options={"require": ["exp"], "verify_signature": True},
                    algorithms=["HS256"],
                )
                return decoded

            else:
                decoded = jwt.decode(
                    jwt=key,
                    key=self.signature,
                    options={"require": ["exp"], "verify_signature": True},
                    algorithms=["HS256"],
                )
                return decoded
        except Exception:
            # Fix status code here
            raise AuthenticationErrors(
                status_code=400, detail={"error": "Invalid key!"}
            )

    def verify_role(self, key: str, path: str) -> bool:
        """Verify user permissions

        Args:
            key (str): jwt key passed
            path (str): verify if jwt is allowed on this path

        Returns:
            bool: is allowed
        """
        try:
            decoded = jwt.decode(
                jwt=key,
                key=self.signature,
                options={"verify_signature": True},
                algorithms=["HS256"],
            )
        except Exception:
            raise AuthenticationErrors(detail={"error": "Invalid key"})
        if "admin" in path:
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
        try:
            old_jwt = self.verify_key(old_token)
        except AuthenticationErrors:
            return False
        payload = {**old_jwt, **payload}
        return self.issue_key(payload=payload)

    def refresh_to_access(
        self, refresh_token: str, payload: Dict[str, Any], expiry: int = 1
    ) -> str:
        """Get new access token from refresh token

        Args:
            refresh_token (str): refresh token provided with access token

        Returns:
            str: new access tokens
        """

        try:
            token = self.verify_key(key=refresh_token)
        except AuthenticationErrors:
            return
        if token.get("refresh"):
            payload["exp"] = (datetime.utcnow() + timedelta(hours=expiry)).timestamp()
            return self.issue_key(payload=payload, get_refresh_token=True)
