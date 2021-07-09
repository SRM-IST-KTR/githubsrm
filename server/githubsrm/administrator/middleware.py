from administrator import jwt_keys
from django.http.response import JsonResponse
from .utils import get_token


class Authorize:
    def __init__(self, view) -> None:
        """
        Initialize requirements
        """
        #! Note: Remember to return JsonResponse from all the paths
        #! That go in this list.
        #! Keep adding Protected routes to this list
        self.protected = ['/admin/projects']
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
                assert token_type == 'Bearer'
                if jwt_keys.verify_key(key=token):
                    return self.view(request)

                return JsonResponse(data={
                    "error": "invalid key"
                }, status=401)
            return JsonResponse(data={
                "error": "token error"
            }, status=401)

        else:
            return self.view(request)
