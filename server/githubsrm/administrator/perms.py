from typing import Callable
from rest_framework.permissions import BasePermission
from .errors import InvalidWebhookError

from administrator import entry
from .utils import get_token
from django.http import request


class AuthAdminPerms(BasePermission):
    def has_permission(self, request: request, view: Callable) -> bool:
        """Check admin register perms

        Args:
            request (request): request object
            view (Callable): view

        Returns:
            bool: has permissions
        """
        token = get_token(request_header=request.headers)
        if token:
            try:
                return entry.check_webHook(token)
            except InvalidWebhookError as e:
                return False
        return False
