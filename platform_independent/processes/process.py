import os
from typing import Union
from windows.local.proc.process import Process as WindowsProcess
from windows.consts import WINDOWS_NAME
from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo, BaseLinuxProcessInfo

LinuxProcess = ''


class Process:
    def __new__(cls, process_info: Union[BaseWindowsProcessInfo, BaseLinuxProcessInfo]):
        if isinstance(process_info, BaseWindowsProcessInfo) and os.name == WINDOWS_NAME:
            WindowsProcess(process_info)
        elif isinstance(process_info, BaseLinuxProcessInfo):
            return LinuxProcess(process_info)
        else:
            raise TypeError(
                "The given process_info must be of type BaseWindowsProcessInfo or BaseLinuxProcessInfo"
                " and match the correct Operating System"
            )
