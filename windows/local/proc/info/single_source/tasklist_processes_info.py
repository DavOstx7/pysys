from __future__ import annotations

from typing import List, Optional, Callable
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from platform_independent.processes.exceptions import FunctionBadArgumentError
from windows.local.proc.info.single_source.tasklist_process_info import TaskListProcessInfo
from windows.local.proc.utils import process_parsing_utils


class TaskListProcessesInfo(BaseWindowsProcessesInfo):
    @staticmethod
    def get_processes_info(find_str_filter: Optional[BaseFindStrFilter] = None) -> List[TaskListProcessInfo]:
        task_list_lines = process_parsing_utils.get_task_list_lines(find_str_filter)
        processes_info: List[TaskListProcessInfo] = [
            TaskListProcessInfo(*process_parsing_utils.parse_task_list_line(task_list_line))
            for task_list_line in task_list_lines
        ]
        return processes_info

    def __init__(self, process_info_list: Optional[TaskListProcessesInfo] = None,
                 find_str_filter: Optional[BaseFindStrFilter] = None):
        if process_info_list:
            processes_info = process_info_list
        else:
            processes_info = self.get_processes_info(find_str_filter)
        super().__init__(processes_info=processes_info)
        self.processes_info: List[TaskListProcessInfo]

    def filter_processes_by_session_name(self, filter_function: Callable[[str], bool],
                                         is_to_return_and_not_set: bool = False) -> Optional[TaskListProcessesInfo]:
        try:
            processes_info: List[TaskListProcessInfo] = [process_info for process_info in self.processes_info
                                                         if filter_function(process_info.session_name)]
            if TaskListProcessesInfo(is_to_return_and_not_set):
                return TaskListProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive str argument 'session_name' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_session_number(self, filter_function: Callable[[int], bool],
                                           is_to_return_and_not_set: bool = False) -> Optional[TaskListProcessesInfo]:
        try:
            processes_info: List[TaskListProcessInfo] = [process_info for process_info in self.processes_info
                                                         if filter_function(process_info.session_number)]
            if is_to_return_and_not_set:
                return TaskListProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'session_number' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_mem_usage_kb(self, filter_function: Callable[[int], bool],
                                         is_to_return_and_not_set: bool = False) -> Optional[TaskListProcessesInfo]:
        try:
            processes_info: List[TaskListProcessInfo] = [process_info for process_info in self.processes_info
                                                         if filter_function(process_info.mem_usage_kb)]
            if is_to_return_and_not_set:
                return TaskListProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'memory_usage_kb' and return true to keep it, else false"
            ) from type_error

