from rest_framework.exceptions import APIException


def set_default_error(detail):
    if not detail:
        return dict(error="Error Occurred!")
    return detail


class ContributorErrors(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class MaintainerErrors(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class MiscErrors(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class ProjectErrors(APIException):
    def __init__(self, status_code=401, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class AuthenticationErrors(APIException):
    def __init__(self, status_code=401, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class AdminErrors(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class ContributorApprovedError(ContributorErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        super().__init__(status_code=status_code, detail=detail)


class ContributorNotFoundError(ContributorErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        super().__init__(status_code=status_code, detail=detail)


class MaintainerNotFoundError(MaintainerErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        super().__init__(status_code=status_code, detail=detail)
