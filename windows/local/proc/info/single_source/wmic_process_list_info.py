from __future__ import annotations

from typing import Union
from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo
from windows.local.proc.info.wmic_extra.wmic_extra_info import WmicExtraInfo
from windows.local.proc.utils import process_parsing_utils
from windows.local.proc.info.single_source.unknown_process_info import UnknownProcessInfo
from platform_independent.processes.exceptions import WmicProcessBriefListFormatError

NODE_ATTR_STR = "node"
HANDLE_COUNT_ATTR_INT = "handle_count"
PRIORITY_ATTR_INT = "priority"
THREAD_COUNT_ATTR_INT = "thread_count"
WORKING_SET_SIZE_KB_ATTR_INT = "working_set_size_kb"


class WmicBriefProcessInfo(BaseWindowsProcessInfo):
    def __init__(self, node: str, handle_count: int, name: str, priority: int, process_id: int, thread_count: int,
                 working_set_size_kb: int, is_constantly_update_wmic_extra: bool = False):
        BaseWindowsProcessInfo.__init__(self, name=name, pid=process_id)

        self.node = node
        self.handle_count = handle_count
        self.priority = priority
        self.thread_count = thread_count
        self.working_set_size_kb = int(working_set_size_kb)
        self.wmic_extra: WmicExtraInfo = WmicExtraInfo(process_id,
                                                       is_constantly_update=is_constantly_update_wmic_extra)

    def get_parent_process_info(self) -> Union[WmicBriefProcessInfo, UnknownProcessInfo]:
        parent_pid: int = self.wmic_extra.parent_pid
        try:
            return WmicBriefProcessInfo(
                *process_parsing_utils.get_parsed_wmic_brief_process_line_by_pid(self.wmic_extra.parent_pid)
            )
        except WmicProcessBriefListFormatError:
            return UnknownProcessInfo(name=f"ParentOf{self.minimal_info}", pid=parent_pid)

    @property
    def working_set_size_mb(self) -> int:
        return self.working_set_size_kb // 1024

    @property
    def str_working_set_size_kb(self) -> str:
        return f"{self.working_set_size_kb} KB"

    @property
    def str_working_set_size_mb(self) -> str:
        return f"{self.working_set_size_mb} MB"

    def __str__(self) -> str:
        return f"{type(self).__name__}(Name = {self.name}, PID = {self.pid}, Priority = {self.priority})"
