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
                          '/admin/projects/accepted', '/maintainer/projects']
        self.view = view

    def __call__(self, request) -> JsonResponse:
        """Middleware to check valid protection

        Args:
            request ([type])

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
        if request.method == 'POST':
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
