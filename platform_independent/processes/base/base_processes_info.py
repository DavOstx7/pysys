from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from platform_independent.processes.base.base_process_info import BaseProcessInfo
from platform_independent.processes.exceptions import FunctionBadArgumentError
from platform_independent.shared.base_filter import BaseFilter


class BaseProcessesInfo(ABC):
    def __init__(self, processes_info: List[BaseProcessInfo]):
        self.processes_info = processes_info

    @staticmethod
    @abstractmethod
    def get_processes_info(processes_filter: Optional[BaseFilter] = None) -> List[BaseProcessInfo]:
        pass

    def refresh(self, processes_filter: Optional[BaseFilter] = None) -> None:
        self.processes_info: List[BaseProcessInfo] = self.get_processes_info(processes_filter)

    def filter_processes_by_name(self, filter_function: Callable[[str], bool],
                                 is_to_return_and_not_set: bool = False) -> Optional[BaseProcessesInfo]:
        try:
            processes_info: List[BaseProcessesInfo] = [process_info for process_info in self.processes_info
                                                       if filter_function(process_info.name)]
            if is_to_return_and_not_set:
                return type(self)(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive str argument 'name' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_pid(self, filter_function: Callable[[int], bool],
                                is_to_return_and_not_set: bool = False) -> Optional[BaseProcessesInfo]:
        try:
            processes_info: List[BaseProcessesInfo] = [process_info for process_info in self.processes_info
                                                       if filter_function(process_info.pid)]
            if is_to_return_and_not_set:
                return type(self)(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive str argument 'name' and return true to keep it, else false"
            ) from type_error

    def __iter__(self):
        return iter(self.processes_info)

    def __str__(self) -> str:
        return type(self).__name__ + \
               "(\n" + f'\n'.join([f"\t{process_info}" for process_info in self.processes_info]) + "\n)"


class BaseWindowsProcessesInfo(BaseProcessesInfo, ABC):
    pass


class BaseLinuxProcessesInfo(BaseProcessesInfo, ABC):
    pass
