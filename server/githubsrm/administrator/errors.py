from core.errorfactory import (
    AuthenticationErrors,
    AdminErrors,
    ContributorErrors,
    MaintainerErrors,
    ProjectErrors,
)


class InvalidWebhookError(AuthenticationErrors):
    ...


class ExistingAdminError(AdminErrors):
    ...


class InvalidAdminCredentialsError(AdminErrors):
    ...


class MaintainerNotFoundError(MaintainerErrors):
    ...


class MaintainerApprovedError(MaintainerErrors):
    ...


class ProjectNotFoundError(ProjectErrors):
    ...


class ContributorNotFoundError(ContributorErrors):
    ...


class ContributorApprovedError(ContributorErrors):
    ...


class InvalidRefreshTokenError(AuthenticationErrors):
    ...


class InvalidUserError(AuthenticationErrors):
    ...
