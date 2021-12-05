from core.errorfactory import (
    ContributorNotFoundError,
    ContributorApprovedError,
    ProjectErrors,
    MaintainerNotFoundError,
    AuthenticationErrors,
    MaintainerErrors,
)


class InvalidMaintainerCredentialsError(AuthenticationErrors):
    def __init__(self, *args, **kwargs):
        self.status_code = 403
        detail = kwargs.get("detail", {"error": "Invalid Maintainer Credentails"})
        super().__init__(detail=detail)
