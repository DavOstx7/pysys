import os
from typing import Optional, Union
from platform_independent.services.base.base_services_info import BaseWindowsServicesInfo, BaseLinuxServicesInfo
from windows.consts import WINDOWS_NAME

LinuxServices = ''
WindowsServices = ''


class Services:
    def __new__(cls, services_info: Optional[Union[BaseWindowsServicesInfo, BaseLinuxServicesInfo]] = None):
        if services_info:
            if isinstance(services_info, BaseWindowsServicesInfo) and os.name == WINDOWS_NAME:
                return WindowsServices(services_info)
            elif isinstance(services_info, BaseLinuxServicesInfo):
                return LinuxServices(services_info)
            else:
                raise TypeError(
                    "The given processes_info must be of type BaseWindowsProcessesInfo or BaseLinuxProcessesInfo"
                    " and match the correct Operating System"
                )
        else:
            if os.name == WINDOWS_NAME:
                return LinuxServices()
            else:
                return WindowsServices()
