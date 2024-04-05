<div align=center>
    <img src="https://github.com/OpenM-Project/librosewater/assets/157366808/f5972377-f93c-4543-88f7-101a6c4c67b3">
</div>

-----

## :inbox_tray: Install
Installation is done through `pip`:
```
pip install git+https://github.com/OpenM-Project/librosewater.git
```
:warning: **WARNING**: This will require you to have `git` in your `PATH`.

## :zap: Example
In this small example, we will:
- Open a process
- Get the address and path of a module loaded into the process
- Dump the module and patch it
- Inject patched module into memory

```py
import os
import ctypes
import librosewater

PID = ... # You can locate this using psutil
process_handle = ctypes.windll.kernel32.OpenProcess(librosewater.PROCESS_ALL_ACCESS, False, PID)

# Get module address and path
module_address, module_path = librosewater.modulehandler.wait_for_module(process_handle, "Windows.ApplicationModel.Store.dll")
module_size = os.stat(module_path).st_size

# Dump module to variable
template = f"Dumping Windows.ApplicationModel.Store module: %s/{module_size}"
data = librosewater.modulehandler.dump_module(process_handle, module_address, module_size, progress=template) # returns as much data as it can

# Inject new module data
new_data = data.replace(b"\x00", b"")
librosewater.inject.inject_module(process_handle, module_address, new_data)
```

## :page_with_curl: License
All code and assets are licensed under GNU AGPLv3.
