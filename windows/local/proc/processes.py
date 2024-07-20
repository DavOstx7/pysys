from __future__ import annotations

from typing import Optional
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo
from windows.consts import FIRST_ELEMENT_INDEX
from windows.local.proc.operations.processes_operations import ProcessesOperations
from windows.local.proc.info.single_source.tasklist_processes_info import TaskListProcessesInfo

DEFAULT_PROCESSES_INFO_CLASS = TaskListProcessesInfo


# Use process_info to create different instances of proc. processes_info can be used as a singleton!

class Processes(ProcessesOperations):
    def __init__(self, processes_info: Optional[BaseWindowsProcessesInfo] = None):
        if not processes_info:
            processes_info = DEFAULT_PROCESSES_INFO_CLASS()
        super().__init__(processes_info)
        self.__process_type = self.get_process_type
        self.__process_info_type = self.get_process_info_type

    def get_process_type(self) -> type:
        process_type = type(self.processes[FIRST_ELEMENT_INDEX])
        if process_type:
            self.__process_type = process_type
        return self.__process_type

    def get_process_info_type(self) -> type:
        process_info_type = type(self.processes[FIRST_ELEMENT_INDEX].process_info)
        if process_info_type:
            self.__process_type = process_info_type
        return self.__process_type

    def __str__(self) -> str:
        return type(self).__name__ + \
               "(\n" + f'\n'.join([f"\t{process}" for process in self.processes]) + "\n)"
