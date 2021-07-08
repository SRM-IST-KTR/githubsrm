from rest_framework.permissions import BasePermission

from administrator import entry


class AdminPerms(BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split()
            assert token[0] == 'Bearer'
            return entry.check_webHook(token[1])
        except Exception as e:
            return False
