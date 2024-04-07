class ReadWriteError(BaseException):
    """
    Raised when read/write to memory has failed.
    """

class QueryError(BaseException):
    """
    Raised when query (moduleinfo etc.) has failed.
    """

class ProtectBypassError(BaseException):
    """
    Raised when protection bypass has failed.
    """

