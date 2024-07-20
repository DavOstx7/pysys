from __future__ import annotations

from abc import ABC, abstractmethod
from platform_independent.services.base.service_state import ServiceState

NAME_ATTRIBUTE_STR = "name"


class BaseServiceInfo(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    @property
    def state(self) -> ServiceState:
        pass

    @property
    def maximal_info(self) -> str:
        return f"{type(self).__name__}" \
               f"({', '.join([f'{key.title()} = {value}' for key, value in self.__dict__.items()])})"

    @property
    def minimal_info(self) -> str:
        return f"<name={self.name}>"

    def __str__(self) -> str:
        return f"{type(self).__name__}(Name = {self.name}"


class BaseWindowsServiceInfo(BaseServiceInfo, ABC):
    pass


class BaseLinuxServiceInfo(BaseServiceInfo, ABC):
    pass
