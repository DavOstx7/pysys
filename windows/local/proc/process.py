from __future__ import annotations

from typing import Optional
from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo
from windows.local.proc.operations.process_operations import ProcessOperations


class Process(ProcessOperations):
    def __init__(self, process_info: BaseWindowsProcessInfo):
        super().__init__(process_info)

    def get_parent_process(self) -> Optional[Process]:
        parent_process_info = self.process_info.get_parent_process_info()
        if parent_process_info:
            return Process(parent_process_info)
        return parent_process_info

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.process_info})"
