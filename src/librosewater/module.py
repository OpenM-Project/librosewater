import os
import ctypes
from ctypes import wintypes
import win32process
from . import *

class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", ctypes.c_void_p),
        ("SizeOfImage", wintypes.DWORD),
        ("EntryPoint", ctypes.c_void_p),
    ]

kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

def wait_for_module(process: int, module_name: str, ignore_reserror: bool = True) -> tuple:
    """
    Blocking function to wait for a module to load.

    Arguments:
    process: int: Process handle for using in pywin32.
    module_name: str: Name of the module file. This will be
    compared to os.path.basepath function result.
    ignore_reserror: bool = True: Ignore module resolution
    errors. This is highly recommended to leave as default,
    first stages of loading in Minecraft can raise a lot of
    these resolution errors.

    Returns tuple class
    (module_address, module_path)
    """
    module = None
    while not module:
        modules = win32process.EnumProcessModulesEx(process)
        for md in modules:
            try:
                name = win32process.GetModuleFileNameEx(process, md)
            except win32process.error as ex:
                if not ignore_reserror:
                    raise ex
            if os.path.basename(name) == module_name:
                return (md, name)

def dump_module(process: int, module: int) -> tuple:
    """
    Dumps module from process memory.

    Arguments:
    process: int: Process handle for using in pywin32.
    module: int: Module address for module.

    Returns tuple class
    (length, data)
    """
    module_info = MODULEINFO()
    if not psapi.GetModuleInformation(process,
            ctypes.c_int64(module), ctypes.byref(module_info)):
        error = ctypes.windll.kernel32.GetLastError()
        raise QueryError("module info query fail, GetModuleInformation return %s" % error)
    dump = ctypes.create_string_buffer(module_info.SizeOfImage)
    if not kernel32.ReadProcessMemory(process, ctypes.c_int64(module_info.lpBaseOfDll),
            ctypes.byref(dump), module_info.SizeOfImage, 0):
        error = ctypes.windll.kernel32.GetLastError()
        raise ReadWriteError("read error, ReadProcessMemory return %s" % error)
    return (module_info.SizeOfImage, dump.raw)

def inject_module(process: int, module: int, data: bytes) -> None:
    """
    Injects module into given address.

    Arguments:
    process: int: Process handle for using in pywin32.
    module: int: Module address for module.
    data: bytes: Bytes for injected module.

    Returns None
    Raises ProtectBypassError on protection bypass fail
    Raises ReadWriteError on write error
    """
    old_security = ctypes.c_int64(PAGE_EXECUTE_READ)
    if not ctypes.windll.kernel32.VirtualProtectEx(process, ctypes.c_int64(module),
            len(data), PAGE_EXECUTE_READWRITE, ctypes.byref(old_security)):
        error = ctypes.windll.kernel32.GetLastError()
        raise ProtectBypassError("security error, VirtualProtectEx return %s" % error)
    if not ctypes.windll.kernel32.WriteProcessMemory(process,
            ctypes.c_int64(module), data, len(data), 0):
        error = ctypes.windll.kernel32.GetLastError()
        raise ReadWriteError("write error, WriteProcessMemory return %s" % error)
