from __future__ import annotations

from typing import Optional, Callable, List
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from platform_independent.processes.exceptions import FunctionBadArgumentError
from windows.local.proc.info.single_source.wmic_process_list_info import WmicBriefProcessInfo
from windows.local.proc.utils import process_parsing_utils


class WmicBriefProcessesInfo(BaseWindowsProcessesInfo):
    @staticmethod
    def get_processes_info(find_str_filter: Optional[BaseFindStrFilter] = None,
                           is_constantly_update_wmic_extra: bool = False) -> List[WmicBriefProcessInfo]:
        wmic_brief_processes_lines = process_parsing_utils.get_wmic_brief_processes_lines(find_str_filter)
        processes_info: List[WmicBriefProcessInfo] = [
            WmicBriefProcessInfo(
                *process_parsing_utils.parse_wmic_brief_process_line(wmic_brief_process_line),
                is_constantly_update_wmic_extra=is_constantly_update_wmic_extra
            )
            for wmic_brief_process_line in wmic_brief_processes_lines
        ]
        return processes_info

    def __init__(self, process_info_list: Optional[WmicBriefProcessesInfo] = None,
                 find_str_filter: Optional[BaseFindStrFilter] = None, is_constantly_update_wmic_extra: bool = False):
        if process_info_list:
            processes_info = process_info_list
        else:
            processes_info = self.get_processes_info(find_str_filter, is_constantly_update_wmic_extra)
        super().__init__(processes_info=processes_info)
        self.processes_info: List[WmicBriefProcessInfo]

    def filter_processes_by_node(self, filter_function: Callable[[str], bool],
                                 is_to_return_and_not_set: bool = False) -> Optional[WmicBriefProcessesInfo]:
        try:
            processes_info: List[WmicBriefProcessInfo] = [process_info for process_info in self.processes_info
                                                          if filter_function(process_info.node)]
            if is_to_return_and_not_set:
                return WmicBriefProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive str argument 'name' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_handle_count(self, filter_function: Callable[[int], bool],
                                         is_to_return_and_not_set: bool = False) -> Optional[WmicBriefProcessesInfo]:
        try:
            processes_info: List[WmicBriefProcessInfo] = [process_info for process_info in self.processes_info
                                                          if filter_function(process_info.handle_count)]
            if is_to_return_and_not_set:
                return WmicBriefProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'pid' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_priority(self, filter_function: Callable[[int], bool],
                                     is_to_return_and_not_set: bool = False) -> Optional[WmicBriefProcessesInfo]:
        try:
            processes_info: List[WmicBriefProcessInfo] = [process_info for process_info in self.processes_info
                                                          if filter_function(process_info.priority)]
            if is_to_return_and_not_set:
                return WmicBriefProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'session_number' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_thread_count(self, filter_function: Callable[[int], bool],
                                         is_to_return_and_not_set: bool = False) -> Optional[WmicBriefProcessesInfo]:
        try:
            processes_info: List[WmicBriefProcessInfo] = [process_info for process_info in self.processes_info
                                                          if filter_function(process_info.thread_count)]
            if is_to_return_and_not_set:
                return WmicBriefProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'memory_usage_kb' and return true to keep it, else false"
            ) from type_error

    def filter_processes_by_working_set_size_kb(self, filter_function: Callable[[int], bool],
                                                is_to_return_and_not_set: bool = False) -> \
            Optional[WmicBriefProcessesInfo]:
        try:
            processes_info: List[WmicBriefProcessInfo] = [process_info for process_info in self.processes_info
                                                          if filter_function(process_info.working_set_size_kb)]
            if is_to_return_and_not_set:
                return WmicBriefProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Given function should receive int argument 'memory_usage_kb' and return true to keep it, else false"
            ) from type_error
