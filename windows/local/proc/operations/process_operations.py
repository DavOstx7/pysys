from platform_independent.processes.base.base_process_operations import BaseProcessOperations

from commands_execution import Output
from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo
from windows.local.proc.utils import process_operations_utils
from windows.variables_packing.taskkill.task_kill_by_pid import TaskKillByPid


class ProcessOperations(BaseProcessOperations):
    def __init__(self, process_info: BaseWindowsProcessInfo):
        self.process_info = process_info

    def kill_process(self) -> Output:
        return self.kill_process_using_task_kill()

    def kill_process_using_task_kill(self, is_force: bool = False, is_include_childs: bool = False) -> Output:
        return process_operations_utils.kill_process_using_task_kill(
            TaskKillByPid(self.process_info.pid, is_force=is_force, is_include_childs=is_include_childs)
        )

    def kill_process_by_pid_using_wmic(self, is_use_terminate_instead_of_delete: bool = False) -> Output:
        return process_operations_utils.kill_process_by_pid_using_wmic(
            self.process_info.pid, is_use_terminate_instead_of_delete
        )
