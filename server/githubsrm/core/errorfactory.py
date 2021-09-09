class ContributorErrors(Exception):
    ...


class MaintainerErrors(Exception):
    ...


class MiscErrors(Exception):
    ...


class ProjectErrors(Exception):
    ...


class AuthenticationErrors(Exception):
    ...


class AdminErrors(Exception):
    ...


class ContributorApprovedError(ContributorErrors):
    ...


class ContributorNotFoundError(ContributorErrors):
    ...


class MaintainerNotFoundError(MaintainerErrors):
    ...
