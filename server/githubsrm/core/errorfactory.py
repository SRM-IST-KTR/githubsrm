from rest_framework.exceptions import APIException

from core.log_utils.log import get_logger


logger = get_logger(
    "custom.exception.logger",
    filename="CustomExceptionLog.log",
    level=20,
)


def set_default_error(detail):
    detail = detail if detail else dict(error="Error!")
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
        logger.info(f"Error occured!\n Exception: {detail}")
        self.status_code = status_code
        super().__init__(detail=detail)


class ProjectErrors(APIException):
    def __init__(self, status_code=401, detail=None):
        detail = set_default_error(detail)
        logger.error(f"Project error! Exception: {detail}")
        self.status_code = status_code
        super().__init__(detail=detail)


class AuthenticationErrors(APIException):
    def __init__(self, status_code=401, detail=None):
        detail = set_default_error(detail)
        logger.info(f"Auth failed!\n Exception: {detail}")
        self.status_code = status_code
        super().__init__(detail=detail)


class AdminErrors(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        logger.error(f"Admin error occured!\n Exception: {detail}")
        self.status_code = status_code
        super().__init__(detail=detail)


class ContributorApprovedError(ContributorErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        logger.info(f"Contributor Already approved!\n Exception {detail}")
        super().__init__(status_code=status_code, detail=detail)


class ContributorNotFoundError(ContributorErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        logger.info(f"Contributor not found!\n Exception {detail}")
        super().__init__(status_code=status_code, detail=detail)


class MaintainerNotFoundError(MaintainerErrors):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail)
        logger.info(f"Maintainer not found!\n Exception {detail}")
        super().__init__(status_code=status_code, detail=detail)


class SchemaError(APIException):
    def __init__(self, status_code=400, detail=None):
        detail = set_default_error(detail, log=False)
        self.status_code = status_code
        super().__init__(detail=detail)
