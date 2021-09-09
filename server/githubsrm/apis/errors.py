from core.errorfactory import ContributorErrors, MaintainerErrors, ProjectErrors
from core.errorfactory import MiscErrors


class ExistingContributorError(ContributorErrors):
    ...


class ApprovedError(ProjectErrors):
    ...


class NotApprovedError(ProjectErrors):
    ...


class ExisitingMaintainerError(MaintainerErrors):
    ...


class ExistingProjectError(ProjectErrors):
    ...
