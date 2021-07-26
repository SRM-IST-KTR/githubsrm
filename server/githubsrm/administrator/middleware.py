from administrator import jwt_keys
from django.http.response import JsonResponse
from .utils import get_token
from apis.utils import check_token
from maintainer.models import Entry

maintainer_entry = Entry()
maintainer_entry = maintainer_entry.db


class Authorize:
    def __init__(self, view) -> None:
        """
        Initialize requirements
        """

        self.protected = ['/admin/projects',
                          '/admin/projects/accepted',
                          '/maintainer/projects']
        self.view = view

    def __call__(self, request) -> JsonResponse:
        """Middleware to check valid protection

        Args:
            request 

        Returns:
            response.Response
        """
        if request.path in self.protected:
            if value := get_token(request_header=request.headers):
                token_type, token = value
                try:
                    assert token_type == 'Bearer'
                except AssertionError as e:
                    return JsonResponse(data={
                        "error": "invalid token type"
                    }, status=401)
                if decoded := jwt_keys.verify_key(key=token) and jwt_keys.verify_role(key=token, path=request.path):
                    request.decoded = decoded
                    return self.view(request)

                else:
                    return JsonResponse(data={
                        "error": "invalid key"
                    }, status=401)
            else:
                return JsonResponse(data={
                    "error": "token error"
                }, status=401)

        else:
            return self.view(request)


class MeVerification:
    def __init__(self, view):
        self.view = view
        self.protected = ['/admin/projects',
                          '/admin/projects/accepted',
                          '/maintainer/projects', "/me"]

    def __call__(self, request, **kwargs) -> JsonResponse:
        """Me verification

        Args:
            request

        Returns:
            JsonResponse
        """
        if request.path in self.protected:
            token = get_token(request_header=request.headers)
            try:
                if token:
                    token_type, token = token
                    assert token_type == "Bearer"
                else:
                    return JsonResponse(data={
                        "error": "No token provided"
                    }, status=401)
            except AssertionError as e:
                return JsonResponse(data={
                    "error": "Invalid token type"
                }, status=401)

            decoded = jwt_keys.verify_key(key=token)
            if decoded:
                request.decoded = decoded
                admin = decoded.get("admin")
                if admin:
                    return self.view(request)
                else:
                    email = decoded.get("email")
                    project_ids = decoded.get("project_id")
                    total_items = maintainer_entry.maintainer.count_documents({
                        "email": email, "is_admin_approved": True
                    })

                if len(project_ids) != total_items:
                    return JsonResponse(data={
                        "error": "Key expired"
                    }, status=401)
                else:
                    request.project_ids = project_ids
                    request.total_items = total_items
                    return self.view(request)
            else:
                return JsonResponse(data={
                    "error": "Invalid Key"
                }, status=401)
        else:
            return self.view(request)


class ReCaptcha:
    def __init__(self, view):
        self.view = view

    def __call__(self, request, **kwargs) -> JsonResponse:
        """Recaptcha middleware

        Args:
            request 

        Returns:
            JsonResponse
        """
        if request.method == 'POST' or request.method == "DELETE":
            try:
                recaptcha = request.META["HTTP_X_RECAPTCHA_TOKEN"]
            except KeyError as e:
                return JsonResponse(data={
                    "error": "recaptcha token not provided"
                }, status=401)

            if check_token(recaptcha):
                return self.view(request)

            else:
                return JsonResponse(data={
                    "error": "invalid recaptcha token"
                }, status=401)
        else:
            return self.view(request)
