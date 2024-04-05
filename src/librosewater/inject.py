import ctypes
from . import *


def inject_module(process: int, module: int, data: bytes) -> None:
    """
    Injects module into given address.

    Arguments:
    process: int: Process handle for using in pywin32.
    module: int: Module address for module.
    data: bytes: Bytes for injected module.

    Returns None
    Raises InjectionFailure on error
    """
    old_security = ctypes.c_int64(PAGE_EXECUTE_READ)
    if not ctypes.windll.kernel32.VirtualProtectEx(process, ctypes.c_int64(module),
            len(data), PAGE_EXECUTE_READWRITE, ctypes.byref(old_security)):
        error = ctypes.windll.kernel32.GetLastError()
        raise InjectionFailure("security error, VirtualProtectEx return %s" % error)
    if not ctypes.windll.kernel32.WriteProcessMemory(process,
            ctypes.c_int64(module), data, len(data), 0):
        error = ctypes.windll.kernel32.GetLastError()
        raise InjectionFailure("write error, WriteProcessMemory return %s" % error)
