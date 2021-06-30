from rest_framework.permissions import BasePermission
import os


class CustomPerms(BasePermission):

    @staticmethod
    def get_perms(token: str) -> bool:
        """Check valid webHook token

        Args:
            token (str): webHook Token

        Returns:
            bool
        """
        valid_token = os.getenv("TOKEN")
        if valid_token == token:
            return True
        return False

    def has_permission(self, request, view):
        """Checks if permissions present

        Args:
            request ([type])
            view ([type])

        Returns:
            bool: Permissions
        """

        try:
            token = request.META.get("HTTP_AUTHORIZATION")

            if self.get_perms(token=token):
                return True
            return False

        except KeyError:
            return False
