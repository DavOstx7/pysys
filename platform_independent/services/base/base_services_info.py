from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from platform_independent.services.base.base_service_info import BaseServiceInfo
from platform_independent.processes.exceptions import FunctionBadArgumentError
from platform_independent.processes.base import BaseProcessesFilter


class BaseServicesInfo(ABC):
    def __init__(self, services_info: List[BaseServiceInfo]):
        self.services_info = services_info

    @staticmethod
    @abstractmethod
    def get_services_info(services_filter: Optional[BaseProcessesFilter] = None) -> List[BaseServiceInfo]:
        pass

    def refresh(self, services_filter: Optional[BaseProcessesFilter] = None) -> None:
        self.services_info: List[BaseServiceInfo] = self.get_services_info(services_filter)

    def filter_service_by_name(self, filter_function: Callable[[str], bool],
                               is_to_return_and_not_set: bool = False) -> Optional[BaseServicesInfo]:
        try:
            services_info: List[BaseServicesInfo] = [service_info for service_info in self.services_info
                                                     if filter_function(service_info.name)]
            if is_to_return_and_not_set:
                return type(self)(services_info)
            else:
                self.services_info = services_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive str argument 'name' and return true to keep it, else false"
            ) from type_error

    def __iter__(self):
        return iter(self.services_info)

    def __str__(self) -> str:
        return type(self).__name__ + \
               "(\n" + f'\n'.join([f"\t{service_info}" for service_info in self.services_info]) + "\n)"


class BaseWindowsServicesInfo(BaseServicesInfo, ABC):
    pass


class BaseLinuxServicesInfo(BaseServicesInfo, ABC):
    pass
