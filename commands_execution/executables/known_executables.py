from commands_execution.executables.executable import Executable

DEFAULT_EXECUTABLE = Executable()

# Linux
SH_NAME, SH_PATH = r"sh", r"/bin/sh"
BASH_NAME, BASH_PATH = r"bash", r"/bin/bash"

# Windows
CMD_NAME, CMD_PATH = r"cmd", r"C:\Windows\System32\cmd.exe"
POWERSHELL_NAME, POWERSHELL_PATH = r"powershell", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
