from core.errorfactory import (
    ContributorNotFoundError,
    ContributorApprovedError,
    ProjectErrors,
    MaintainerNotFoundError,
    AuthenticationErrors,
    MaintainerErrors,
)


class InvalidMaintainerCredentialsError(MaintainerErrors):
    ...
