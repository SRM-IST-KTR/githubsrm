from core.errorfactory import (
    AuthenticationErrors,
    AdminErrors,
    MaintainerErrors,
    ProjectErrors,
    ContributorApprovedError,
    ContributorNotFoundError,
    MaintainerNotFoundError,
)


class InvalidWebhookError(AuthenticationErrors):
    def __init__(self, *args, **kwargs):
        status_code = 401
        detail = kwargs.get("detail", {"Invalid WebHook!"})
        super().__init__(detail=detail, status_code=status_code)


class ExistingAdminError(AdminErrors):
    def __init__(self, *args, **kwargs):
        self.status_code = 409
        detail = kwargs.get("detail", {"error": "Admin already exists!"})
        super().__init__(detail=detail)


class InvalidAdminCredentialsError(AuthenticationErrors):
    def __init__(self, *args, **kwargs):
        detail = kwargs.get("detail", {"error": "Invalid credentials"})
        super().__init__(detail=detail)


class MaintainerApprovedError(MaintainerErrors):
    def __init__(self, *args, **kwargs):
        self.status_code = 400
        detail = kwargs.get("detail", {"error": "Maintainer Already Approved!"})
        super().__init__(detail=detail)


class ProjectNotFoundError(ProjectErrors):
    def __init__(self, *args, **kwargs):
        self.status_code = 400
        detail = kwargs.get("detail", {"error": "Project not found!"})
        super().__init__(detail=detail)


class InvalidRefreshTokenError(AuthenticationErrors):
    def __init__(self, *args, **kwargs):
        detail = kwargs.get("detail", {"error": "Invalid refresh token!"})
        super().__init__(detail=detail)


class InvalidUserError(AuthenticationErrors):
    def __init__(self, *args, **kwargs):
        detail = kwargs.get("detail", {"error": "Invalid User!"})
        super().__init__(detail=detail)


class InvalidMember(AdminErrors):
    def __init__(self, *args, **kwargs):
        detail = kwargs.get("detail", {"error": "Invalid Member!"})
        super().__init__(detail=detail)
