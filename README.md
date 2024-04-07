<div align=center>
    <img src="https://github.com/OpenM-Project/librosewater/assets/157366808/f5972377-f93c-4543-88f7-101a6c4c67b3">
</div>

-----

## :construction: Status
The project is going a rewrite at the moment, and you can expect things to break.

All users migrating from 0.1.x should take a look at the new example to adapt their code.

Current changes:
- Chunksize has been removed
- Partially migrated to ctypes *(from pywin32)*
- Renamed modulehandler to module
- Moved injection handler to module
- Added new Exception classes

## :computer: Support
The library only works on Windows for now, but cross-platform support is planned. ~~Don't look forward to it, though.~~

For all support needed to this library, you can open an issue!
And you can join our [Discord](https://dsc.gg/openm "OpenM Community") server
for further support needed.

## :inbox_tray: Install
Installation is done through `pip`:
```
pip install git+https://github.com/OpenM-Project/librosewater.git
```
:warning: **WARNING**: This will require you to have [`git`](https://git-scm.com/downloads) in your `PATH`.

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
import librosewater.module

PID = ... # You can locate this using psutil
process_handle = ctypes.windll.kernel32.OpenProcess(librosewater.PROCESS_ALL_ACCESS, False, PID)

# Get module address and path
module_address, module_path = librosewater.module.wait_for_module(process_handle, "Windows.ApplicationModel.Store.dll")
module_size = os.stat(module_path).st_size

# Dump module to variable
data_length, data = librosewater.module.dump_module(process_handle, module_address)

# Inject new module data
new_data = data.replace(b"\x00", b"")
librosewater.module.inject_module(process_handle, module_address, new_data)
```

## :page_with_curl: License
All code and assets are licensed under GNU AGPLv3.
