import os
from typing import Union
from windows.consts import WINDOWS_NAME
from platform_independent.services.base.base_service_info import BaseWindowsServiceInfo, BaseLinuxServiceInfo

WindowsService = ''
LinuxService = ''


class Service:
    def __new__(cls, service_info: Union[BaseWindowsServiceInfo, BaseLinuxServiceInfo]):
        if isinstance(service_info, BaseWindowsServiceInfo) and os.name == WINDOWS_NAME:
            WindowsService(service_info)
        elif isinstance(service_info, BaseLinuxServiceInfo):
            return LinuxService(service_info)
        else:
            raise TypeError(
                "The given service_info must be of type BaseWindowsServiceInfo or BaseLinuxServiceInfo"
                " and match the correct Operating System"
            )
