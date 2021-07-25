from django.http.response import JsonResponse
from administrator.utils import get_token
from . import entry
from administrator import jwt_keys

entry = entry.db

class VerifyMaintainer:
    def __init__(self, view):
        self.view = view
        self.coverage = [
            "/maintainer/projects", "/maintainer/me"
        ]

    def __call__(self, request, **kwargs) -> JsonResponse:
        """Verify maintiner jwt with project ids

        Args:
            request 

        Returns:
            JsonResponse
        """
        if request.path in self.coverage and request.method == "GET":
            token_type, token = get_token(request_header=request.headers)
            decoded = jwt_keys.verify_key(token)
            if decoded:
                try:
                    project_ids = decoded["project_id"]
                    email = decoded["email"]
                except KeyError as e:
                    return JsonResponse(data={
                        "error": "Inconsistant data"
                    }, status=401)

                total_items = entry.maintainer.count_documents({
                    "email": email, "is_admin_approved": True
                })

                if total_items > len(project_ids):
                    return JsonResponse(data={
                        "error": "Key expired"
                    }, status=401)

                else:
                    request.project_ids = project_ids
                    request.total_items = total_items
                    return self.view(request)
            else:
                return JsonResponse(data={
                    "error": "Invalid key"
                }, status=401)
        else:
            return self.view(request)
