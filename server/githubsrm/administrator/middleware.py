from administrator import jwt_keys
from rest_framework import response, status
from .utils import get_token


class Authorize:
    def __init__(self, view) -> None:
        """
        Initialize requirements
        """
        # Keep adding proectedted routes to this list
        self.protected = ['project']
        self.view = view

    def __call__(self, request) -> response.Response:
        """Middleware to check valid protection

        Args:
            request ([type])

        Returns:
            response.Response
        """

        if request.path in self.protected:
            if value := get_token(request_header=request.header):
                token_type, token = value
                assert token_type == 'Bearer'
                if jwt_keys.verify_key(key=token):
                    return self.view(request)
                return response.Response(data={
                    "invalid key"
                }, status=status.HTTP_401_UNAUTHORIZED)
            return response.Response(data={
                "invalid token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return self.view(request)
