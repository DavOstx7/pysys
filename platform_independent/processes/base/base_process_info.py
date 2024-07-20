from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

NAME_ATTRIBUTE_STR = "name"
PID_ATTRIBUTE_INT = "pid"


class BaseProcessInfo(ABC):

    def __init__(self, name: str, pid: int):
        self.pid = pid
        self.name = name

    @abstractmethod
    def get_parent_process_info(self) -> Optional[BaseProcessInfo]:
        pass

    @property
    def maximal_info(self) -> str:
        return f"{type(self).__name__}" \
               f"({', '.join([f'{key.title()} = {value}' for key, value in self.__dict__.items()])})"

    @property
    def minimal_info(self) -> str:
        return f"<name={self.name}>, pid={self.pid}>"

    def __str__(self) -> str:
        return f"{type(self).__name__}(Name = {self.name}, PID = {self.pid})"


class BaseWindowsProcessInfo(BaseProcessInfo, ABC):
    pass


class BaseLinuxProcessInfo(BaseProcessInfo, ABC):
    pass
