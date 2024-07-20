from __future__ import annotations

from typing import Union
from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo
from windows.local.proc.utils import process_info_utils, process_parsing_utils
from platform_independent.processes.exceptions import TaskListFormatError
from windows.local.proc.info.single_source.unknown_process_info import UnknownProcessInfo

SESSION_NAME_ATTR_STR = "session_name"
SESSION_NUMBER_ATTR_INT = "session_number"
MEM_USAGE_KB_ATTR_INT = "mem_usage_kb"


class TaskListProcessInfo(BaseWindowsProcessInfo):
    def __init__(self, image_name: str, pid: int, session_name: str, session_number: int, mem_usage_kb: int):
        BaseWindowsProcessInfo.__init__(self, name=image_name, pid=pid)

        self.session_name = session_name
        self.session_number = session_number
        self.mem_usage_kb = mem_usage_kb

    def get_parent_process_info(self) -> Union[TaskListProcessInfo, UnknownProcessInfo]:
        parent_pid = process_info_utils.get_parent_process_id(self.pid)
        try:
            return TaskListProcessInfo(*process_parsing_utils.get_parsed_task_list_line_by_pid(parent_pid))
        except TaskListFormatError:
            return UnknownProcessInfo(name=f"ParentOf{self.minimal_info}", pid=parent_pid)

    @property
    def mem_usage_mb(self) -> int:
        return self.mem_usage_kb // 1024

    @property
    def str_mem_usage_kb(self) -> str:
        return f"{self.mem_usage_kb} KB"

    @property
    def str_mem_usage_mb(self) -> str:
        return f"{self.str_mem_usage_mb} MB"

    def __str__(self) -> str:
        return f"{type(self).__name__}" \
               f"(Image Name = {self.name}, PID = {self.pid}, Mem Usage = {self.str_mem_usage_kb})"
