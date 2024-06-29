import os
import ctypes
from ctypes import wintypes
from . import *

def wait_for_process(process_name: str) -> tuple:
    """
    Blocking function to wait for a process.

    Arguments:
    process_name: str: Name of the process to wait for.

    Returns tuple class
    (process_pid, process_handle)
    """
    while True:
        count = 32
        while True:
            loaded_processes = (wintypes.DWORD * count)()
            loaded_processes_size = ctypes.sizeof(loaded_processes)
            cb_needed = wintypes.DWORD()
            if not psapi.EnumProcesses(ctypes.byref(loaded_processes), loaded_processes_size, ctypes.byref(cb_needed)):
                error = ctypes.windll.kernel32.GetLastError()
                raise QueryError("process list query fail, EnumProcesses return %s" % error)
            if cb_needed.value < loaded_processes_size:
                break
            else:
                count *= 2

        for x in range(cb_needed.value // ctypes.sizeof(ctypes.wintypes.DWORD)):
            proc = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, loaded_processes[x])
            if proc:
                proc_name = (ctypes.c_char * MAX_PATH)()
                if psapi.GetProcessImageFileNameA(proc, proc_name, MAX_PATH):
                    if process_name == os.path.basename(proc_name.value.decode()):
                        return (loaded_processes[x], proc)
                kernel32.CloseHandle(proc)
