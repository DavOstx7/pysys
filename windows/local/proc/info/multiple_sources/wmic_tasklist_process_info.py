from __future__ import annotations

from typing import Tuple, Union
from windows.local.proc.info.single_source.tasklist_process_info import TaskListProcessInfo
from windows.local.proc.info.single_source.wmic_process_list_info import WmicBriefProcessInfo
from windows.local.proc.utils import process_parsing_utils
from windows.local.proc.info.single_source.unknown_process_info import UnknownProcessInfo
from platform_independent.processes.exceptions import WmicProcessBriefListFormatError, TaskListFormatError


class WmicAndTaskListProcessInfo(WmicBriefProcessInfo, TaskListProcessInfo):
    def __init__(self, *, wmic_brief_process_arguments: Tuple[str, int, str, int, int, int, int],
                 task_list_arguments: Tuple[str, int, str, int, int],
                 is_constantly_update_wmic_extra: bool = False):
        WmicBriefProcessInfo.__init__(self, *wmic_brief_process_arguments,
                                      is_constantly_update_wmic_extra=is_constantly_update_wmic_extra)
        TaskListProcessInfo.__init__(self, *task_list_arguments)

    def get_parent_process_info(self) -> Union[WmicAndTaskListProcessInfo, UnknownProcessInfo]:
        parent_pid: int = self.wmic_extra.parent_pid
        try:
            return WmicAndTaskListProcessInfo(
                wmic_brief_process_arguments=process_parsing_utils.get_parsed_wmic_brief_process_line_by_pid(
                    parent_pid
                ),
                task_list_arguments=process_parsing_utils.get_parsed_task_list_line_by_pid(parent_pid)
            )
        except WmicProcessBriefListFormatError or TaskListFormatError:
            return UnknownProcessInfo(name=f"ParentOf{self.minimal_info}", pid=parent_pid)

    def __str__(self) -> str:
        return f"{type(self).__name__}" \
               f"(Name = {self.name}, PID = {self.pid}, Priority = {self.priority}, Mem Usage = {self.str_mem_usage_kb})"
