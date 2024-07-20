from commands_execution import Executor, Output
from windows.variables_packing.taskkill.base.base_task_kill import BaseTaskKill
from windows.consts import SHORT_TIMEOUT

CMD = Executor()


def kill_process_using_task_kill(task_kill: BaseTaskKill) -> Output:
    return CMD.execute_command_simply(task_kill.get_task_kill_command(), timeout=SHORT_TIMEOUT)


def kill_process_by_name_using_wmic(name_expression: str,
                                    is_use_terminate_instead_of_delete: bool = False,
                                    is_use_like_for_comparison: bool = False) -> Output:
    wmic_command = f"wmic process "
    wmic_command += f'where "Name Like \'{name_expression}\'" ' if is_use_like_for_comparison \
        else f'where name="{name_expression}" '
    wmic_command += "call terminate" if is_use_terminate_instead_of_delete else "delete"
    return CMD.execute_command_simply(wmic_command, timeout=SHORT_TIMEOUT)


def kill_process_by_pid_using_wmic(pid: int, is_use_terminate_instead_of_delete: bool = False) -> Output:
    wmic_command = f"wmic process where (ProcessId={pid}) "
    wmic_command += "call terminate" if is_use_terminate_instead_of_delete else "delete"
    return CMD.execute_command_simply(wmic_command, timeout=SHORT_TIMEOUT)
