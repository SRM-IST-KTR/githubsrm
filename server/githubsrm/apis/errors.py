from core.errorfactory import ContributorErrors, MaintainerErrors, ProjectErrors
from core.errorfactory import MiscErrors


class ExistingContributorError(ContributorErrors):
    def __init__(self, detail):
        super().__init__(status_code=409, detail=detail)


class ApprovedError(ProjectErrors):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)


class NotApprovedError(ProjectErrors):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)


class ExisitingMaintainerError(MaintainerErrors):
    def __init__(self, detail):
        super().__init__(status_code=409, detail=detail)


class ExistingProjectError(ProjectErrors):
    def __init__(self, detail):
        super().__init__(status_code=409, detail=detail)


class InvalidProjectId(ProjectErrors):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)
