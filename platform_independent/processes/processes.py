import os
from typing import Optional, Union
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo, BaseLinuxProcessesInfo
from windows.local.proc.processes import Processes as WindowsProcesses
from windows.consts import WINDOWS_NAME

LinuxProcesses = ''


class Processes:
    def __new__(cls, processes_info: Optional[Union[BaseWindowsProcessesInfo, BaseLinuxProcessesInfo]] = None):
        if processes_info:
            if isinstance(processes_info, BaseWindowsProcessesInfo) and os.name == WINDOWS_NAME:
                return WindowsProcesses(processes_info)
            elif isinstance(processes_info, BaseLinuxProcessesInfo):
                return BaseWindowsProcessesInfo
            else:
                raise TypeError(
                    "The given processes_info must be of type BaseWindowsProcessesInfo or BaseLinuxProcessesInfo"
                    " and match the correct Operating System"
                )
        else:
            if os.name == WINDOWS_NAME:
                return WindowsProcesses()
            else:
                return LinuxProcesses()
