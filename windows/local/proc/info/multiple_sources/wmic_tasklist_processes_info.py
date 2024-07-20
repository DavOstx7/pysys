from __future__ import annotations

from typing import Optional, List, Tuple, Callable, Union
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from windows.local.proc.info.multiple_sources.wmic_tasklist_process_info import WmicAndTaskListProcessInfo
from platform_independent.processes.exceptions import FunctionBadArgumentError
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo
from windows.local.proc.utils import process_parsing_utils
from windows.local.proc.consts import TASK_LIST_WMIC_PROCESS_INFO_ATTRIBUTES
from windows.consts import FIRST_ELEMENT_INDEX
from windows.local.proc.consts import TASK_LIST_CSV_FORMAT, WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT,  NON_ZIPPED_LINES_KEY
from windows.local.proc.info.single_source.tasklist_process_info import TaskListProcessInfo
from windows.local.proc.info.single_source.wmic_process_list_info import WmicBriefProcessInfo
from platform_independent.processes.exceptions import WmicProcessBriefListFormatError

TASK_LIST_CSV_FORMAT: str = TASK_LIST_CSV_FORMAT
WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT: str = WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT
PROCESS_ATTRIBUTES_LISTED: List[str] = TASK_LIST_WMIC_PROCESS_INFO_ATTRIBUTES


class WmicAndTaskListProcessesInfo(BaseWindowsProcessesInfo):
    @staticmethod
    def get_processes_info(find_str_filter: Optional[BaseFindStrFilter] = None,
                           is_constantly_update_wmic_extra: bool = False) -> \
            Tuple[List[WmicAndTaskListProcessInfo], List[str]]:
        pid_to_matching_lines_mapper = process_parsing_utils.get_zipped_matching_task_list_and_wmic_brief_lines()
        non_zipped_lines = pid_to_matching_lines_mapper.pop(NON_ZIPPED_LINES_KEY)
        sorted_zipped_matching_lines = sorted(
            pid_to_matching_lines_mapper.items(), key=lambda pid_and_lines_pair: pid_and_lines_pair[FIRST_ELEMENT_INDEX]
        )
        processes_info: List[WmicAndTaskListProcessInfo] = []
        for (_, (task_list_line, wmic_brief_process_line)) in sorted_zipped_matching_lines:
            process_info: WmicAndTaskListProcessInfo = WmicAndTaskListProcessInfo(
                task_list_arguments=process_parsing_utils.parse_task_list_line(task_list_line),
                wmic_brief_process_arguments=process_parsing_utils.parse_wmic_brief_process_line(
                    wmic_brief_process_line
                ),
                is_constantly_update_wmic_extra=is_constantly_update_wmic_extra
            )
            processes_info.append(process_info)
        return processes_info, non_zipped_lines

    @staticmethod
    def create_processes_info_from_wmic_or_task_list_lines(lines: List[Union[str, bytes]],
                                                           is_constantly_update_wmic_extra: bool = False) -> \
            List[Union[WmicBriefProcessInfo, TaskListProcessInfo]]:
        processes_info = []
        for line in lines:
            try:
                process_info = WmicBriefProcessInfo(
                    *process_parsing_utils.parse_wmic_brief_process_line(line),
                    is_constantly_update_wmic_extra=is_constantly_update_wmic_extra
                )
            except WmicProcessBriefListFormatError:
                process_info = TaskListProcessInfo(*process_parsing_utils.parse_task_list_line(line))
            processes_info.append(process_info)
        return processes_info

    def __init__(self, process_info_list: Optional[WmicAndTaskListProcessInfo] = None,
                 find_str_filter: Optional[BaseFindStrFilter] = None, is_constantly_update_wmic_extra: bool = False):
        if process_info_list:
            processes_info = process_info_list
            non_zipped_lines = []
        else:
            processes_info, non_zipped_lines = self.get_processes_info(find_str_filter,
                                                                       is_constantly_update_wmic_extra)
        super().__init__(processes_info=processes_info)
        self.non_zipped_processes_info = self.create_processes_info_from_wmic_or_task_list_lines(non_zipped_lines)
        self.processes_info: List[WmicAndTaskListProcessInfo]

    def filter_processes_by_attribute(self, attribute: str, filter_function: Callable[[Union[str, int]], bool],
                                      is_to_return_and_not_set: bool = False) -> \
            Optional[WmicAndTaskListProcessesInfo]:
        try:
            processes_info: List[WmicAndTaskListProcessInfo] = [process_info for process_info in self.processes_info
                                                                if filter_function(getattr(process_info, attribute))]
            if is_to_return_and_not_set:
                return WmicAndTaskListProcessesInfo(processes_info)
            else:
                self.processes_info = processes_info
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "Bad typing done! Make sure to use a correct attribute-to-type correlation in the filtering"
            ) from type_error
        except AttributeError as attribute_error:
            raise AttributeError(
                f"The given attribute does not exist! Here are the options: {TASK_LIST_WMIC_PROCESS_INFO_ATTRIBUTES}"
            ) from attribute_error
