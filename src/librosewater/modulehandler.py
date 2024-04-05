import os
import win32process
from .exceptions import *

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

def dump_module(process: int, module: int, size: int,
                chunksize: int = 10240, progress: str = '') -> tuple:
    """
    Dumps module from process memory, then returns
    as much dumped data as possible.

    Arguments:
    process: int: Process handle for using in pywin32.
    module: int: Module address for module.
    size: int: Size of module to be dumped.
    chunksize: int = 10240: Chunk size for dumping memory.
    Lower values can read more memory, but higher values
    are faster to run. Recommended to use default value.
    progress: str = '': Format string for byte progress.
    Will display on the same line by default.
    Example value: "Progress: %s/923174 bytes"

    Returns tuple class
    (length, data)
    """
    index = start = module
    data = b''
    while True:
        try:
            readdata = win32process.ReadProcessMemory(process, index, chunksize)
            if progress:
                print(progress % (index-start), end="\r")
        except win32process.error:
            if progress:
                print(progress % (index-start))
            break
        index += chunksize
        data += readdata
    return (index - start, data)
