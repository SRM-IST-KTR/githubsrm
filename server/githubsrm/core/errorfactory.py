from rest_framework.exceptions import APIException


class ContributorErrors(APIException):
    def __init__(self, detail="Error Occoured!", code=400):
        super().__init__(detail=detail, code=code)


class MaintainerErrors(APIException):
    def __init__(self, detail="Error Occoured!", code=400):
        super().__init__(detail=detail, code=code)


class MiscErrors(APIException):
    def __init__(self, detail="Error Occoured!", status_code=400):
        self.status_code = status_code
        super().__init__(detail=detail)


class ProjectErrors(APIException):
    def __init__(self, detail="Error Occoured!", code=400):
        super().__init__(detail=detail, code=code)


class AuthenticationErrors(APIException):
    def __init__(self, detail="Error Occoured!", status_code=403):
        self.status_code = status_code
        super().__init__(detail=detail)


class AdminErrors(APIException):
    def __init__(self, detail="Error Occoured!", status_code=400):
        self.status_code = status_code
        super().__init__(detail=detail)


class ContributorApprovedError(ContributorErrors):
    def __init__(self, detail="Error Occoured!", status_code=400):
        self.status_code = status_code
        super().__init__(detail=detail)


class ContributorNotFoundError(ContributorErrors):
    def __init__(self, detail="Error Occoured!", status_code=400):
        self.status_code = status_code
        super().__init__(detail=detail)



class MaintainerNotFoundError(MaintainerErrors):
    def __init__(self, detail="Error Occoured!", status_code=400):
        self.status_code = status_code
        super().__init__(detail=detail)
