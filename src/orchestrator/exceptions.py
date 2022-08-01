from datetime import datetime


class BaseException(Exception):
    def __init__(self, code=None, error_message=None, message=None, timestamp=None):
        self.code = code
        self.message = message
        self.error_message = error_message
        if not timestamp:
            self.timestamp = str(datetime.now())
        else:
            self.timestamp = timestamp
        super().__init__(message)

    def __str__(self):
        return f"\nException Type: {type(self).__name__}\nException Code: {self.code}\nException Message: {self.message}\nTimestamp: {self.timestamp}\nError Message: {self.error_message}"


class OrchestratorAuthException(BaseException):
    def __init__(self, code="authentication_error", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorInvalidODataException(BaseException):
    def __init__(self, code="odata_error", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorMissingParameters(BaseException):
    def __init__(self, code="missing_parameters", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorFolderNotFound(BaseException):
    def __init__(self, code="folder_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorInsufficientPermissions(BaseException):
    def __init__(self, code="insufficient_permissions", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorQueueNotFound(BaseException):
    def __init__(self, code="queue_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorAssetNotFound(BaseException):
    def __init__(self, code="asset_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorServerUnavailable(BaseException):
    def __init__(self, code="server_unavailable", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorProcessNotFound(BaseException):
    def __init__(self, code="process_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorProcessScheduleNotFound(BaseException):
    def __init__(self, code="schedule_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)


class OrchestratorJobNotFound(BaseException):
    def __init__(self, code="job_not_found", message=None, error_message=None):
        super().__init__(code=code, message=message, error_message=error_message)
