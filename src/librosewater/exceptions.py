class ReadWriteError(Exception):
    """
    Raised when read/write to memory has failed.
    """

class QueryError(Exception):
    """
    Raised when query (moduleinfo etc.) has failed.
    """

class ProtectBypassError(Exception):
    """
    Raised when protection bypass has failed.
    """

class ProcessClosedError(Exception):
    """
    Raised when passed process handle reports closed status.
    """
