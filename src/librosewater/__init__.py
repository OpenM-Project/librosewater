import ctypes
from .exceptions import *

MAX_PATH = 260
LIST_MODULES_ALL = 3
PROCESS_ALL_ACCESS = 0x1F0FFF
PAGE_EXECUTE_READ = 0x20
PAGE_EXECUTE_READWRITE = 0x40

kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

__version__ = "0.3.2"
