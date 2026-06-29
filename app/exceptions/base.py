class AIException(Exception):
    def __init__(self, message: str, code: str = "UNKNOWN", details: dict = None):
        self.code = code
        self.details = details or {}
        super().__init__(message)


class ServiceException(AIException):
    def __init__(self, message: str, code: str = "SERVICE_ERROR", details: dict = None):
        super().__init__(message, code=code, details=details)


class ToolException(AIException):
    def __init__(self, message: str, code: str = "TOOL_ERROR", details: dict = None):
        super().__init__(message, code=code, details=details)


class LLMException(AIException):
    def __init__(self, message: str, code: str = "LLM_ERROR", details: dict = None):
        super().__init__(message, code=code, details=details)


class MemoryException(AIException):
    def __init__(self, message: str, code: str = "MEMORY_ERROR", details: dict = None):
        super().__init__(message, code=code, details=details)
