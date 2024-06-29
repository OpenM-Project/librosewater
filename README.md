<div align=center>
    <img src="https://github.com/OpenM-Project/librosewater/assets/157366808/f5972377-f93c-4543-88f7-101a6c4c67b3">
</div>

-----

## :computer: Support
The library only works on Windows for now, but cross-platform support may be added in the future. ~~Don't look forward to it, though.~~

For all support needed to this library, you can open an [issue](https://github.com/OpenM-Project/librosewater/issues/), or you can join our [Discord](https://dsc.gg/openmproject "OpenM Community") server or [subreddit](https://www.reddit.com/r/openmproject/) for any further support needed.

## :inbox_tray: Install
Installation is done through `pip`:
```
pip install git+https://github.com/OpenM-Project/librosewater.git
```
:warning: **WARNING**: This will require you to have [`git`](https://git-scm.com/downloads) in your `PATH`.

## :zap: Example
In this small example, we will:
- Wait for a process to start
- Open the process
- Get the address and path of a module loaded into the process
- Dump the module and patch it
- Inject patched module into memory

```py
import ctypes
import librosewater
import librosewater.module
import librosewater.process

PID = librosewater.process.wait_for_process("my_app.exe")
process_handle = ctypes.windll.kernel32.OpenProcess(librosewater.PROCESS_ALL_ACCESS, False, PID)

# Get module address and path
module_address, module_path = librosewater.module.wait_for_module(process_handle, "super_secret_stuff.dll")

# Dump module to variable
data_length, data = librosewater.module.dump_module(process_handle, module_address)

# Inject new module data
new_data = data.replace(b"\x00", b"\x02")
librosewater.module.inject_module(process_handle, module_address, new_data)
```

## :page_with_curl: License
All code and assets are licensed under GNU AGPLv3.
