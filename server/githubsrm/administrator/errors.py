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
    ...


class ExistingAdminError(AdminErrors):
    ...


class InvalidAdminCredentialsError(AdminErrors):
    ...


class MaintainerApprovedError(MaintainerErrors):
    ...


class ProjectNotFoundError(ProjectErrors):
    ...


class InvalidRefreshTokenError(AuthenticationErrors):
    ...


class InvalidUserError(AuthenticationErrors):
    ...
