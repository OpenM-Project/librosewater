import os
import ctypes
from ctypes import wintypes
from . import *

class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", ctypes.c_void_p),
        ("SizeOfImage", wintypes.DWORD),
        ("EntryPoint", ctypes.c_void_p),
    ]

kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

def wait_for_module(process: int, module_name: str,
    modulelist_num: int = 3) -> tuple:
    """
    Blocking function to wait for a module to load.

    Arguments:
    process: int: Process handle for using in pywin32.
    module_name: str: Name of the module file. This will be
    compared to os.path.basepath function result.
    modulelist_num: int = 3: Multiplier for module list.
    Gets multiplied by 512 bytes and used as module list
    size. Change this if your module doesn't show up for
    any reason, should be fine for most apps

    Returns tuple class
    (module_address, module_path)
    """
    module = None
    while not module:
        modulelist_size = 512 * modulelist_num
        modulelist = (wintypes.HMODULE * modulelist_size)()
        if not psapi.EnumProcessModulesEx(process, ctypes.byref(modulelist),
                modulelist_size, ctypes.byref(wintypes.DWORD()), LIST_MODULES_ALL):
            error = ctypes.windll.kernel32.GetLastError()
            raise QueryError("module enum query fail, EnumProcessModulesEx return %s" % error)
        for md in modulelist:
            if not md:
                continue
            name = ctypes.create_unicode_buffer(MAX_PATH)
            if not psapi.GetModuleFileNameExW(process,
                    ctypes.c_int64(md), name, MAX_PATH):
                continue
            if os.path.basename(name.value) == module_name:
                return (md, name.value)

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
