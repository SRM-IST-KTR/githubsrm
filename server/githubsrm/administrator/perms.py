from rest_framework.permissions import BasePermission

from administrator import entry
from .utils import get_token


class RegisterAdminPerms(BasePermission):
    def has_permission(self, request, view):

        try:

            if value := get_token(request_header=request.headers):
                token_type, token = value
                assert token_type == 'Bearer'
                return entry.check_webHook(token)
            return False

        except Exception as e:
            return False
