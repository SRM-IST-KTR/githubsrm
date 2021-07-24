from administrator import jwt_keys
from django.http.response import JsonResponse
from .utils import get_token
from apis.utils import check_token


class Authorize:
    def __init__(self, view) -> None:
        """
        Initialize requirements
        """

        self.protected = ['/admin/projects',
                          '/admin/projects/accepted',
                          '/maintainer/projects']
        self.view = view

    @staticmethod
    def _refresh_route(request, view):
        if token := get_token(request_headers=request.headers):
            token_type, token = token
        else:
            return JsonResponse(data={
                "error": "token not provided"
            }, status=401)

        try:
            assert token_type == "Bearer"
        except AssertionError as e:
            return JsonResponse(data={
                "error": "Invalid token type"
            }, status=401)

        decoded = jwt_keys.verify_key(key=token)
        if decoded:
            if decoded.get("refresh"):
                return view(request)
            else:
                return JsonResponse(data={
                    "error": "Invalid token"
                }, status=401)
        else:
            return JsonResponse(data={
                "error": "Invalid token"
            }, status=401)

    def __call__(self, request) -> JsonResponse:
        """Middleware to check valid protection

        Args:
            request 

        Returns:
            response.Response
        """

        if request.path == "/maintainer/refresh-token":
            self._refresh_route(request, self.view)

        if request.path in self.protected:
            if value := get_token(request_header=request.headers):
                token_type, token = value
                try:
                    assert token_type == 'Bearer'
                except AssertionError as e:
                    return JsonResponse(data={
                        "error": "invalid token type"
                    }, status=401)
                if jwt_keys.verify_key(key=token) and jwt_keys.verify_role(key=token, path=request.path):
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
