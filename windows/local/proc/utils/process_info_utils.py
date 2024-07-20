from typing import Optional, List
from commands_execution import Executor, Output
from commands_execution.exceptions import CommandTimeoutError
from platform_independent.shared.utils import pipe_filter_to_command, retry
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from windows.variables_packing.findstr.regex_findstr_filter import RegexFindStrFilter
from windows.consts import SHORT_TIMEOUT, MEDIUM_TIMEOUT, LONG_TIMEOUT, NEW_LINE
from windows.local.proc.consts import TASK_LIST_COMMAND, VERBOSE_TASK_LIST_COMMAND
from windows.local.proc.consts import WMIC_PROCESS_LIST_BRIEF_COMMAND, WMIC_PROCESS_GET_COMMAND
from windows.local.proc.consts import WMIC_PROCESS_LIST_COMMAND

CMD = Executor()


@retry(times=1, exceptions={CommandTimeoutError})
def task_list(find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    full_command = pipe_filter_to_command(TASK_LIST_COMMAND, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=SHORT_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def verbose_task_list(find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    full_command = pipe_filter_to_command(VERBOSE_TASK_LIST_COMMAND, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=LONG_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_process_brief_list(find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    full_command = pipe_filter_to_command(WMIC_PROCESS_LIST_BRIEF_COMMAND, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=SHORT_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_process_list(find_str_filter: Optional[BaseFindStrFilter], list_format: Optional[str] = None):
    wmic_process_list_command = WMIC_PROCESS_LIST_COMMAND
    if list_format:
        wmic_process_list_command += f" {list_format}"
    full_command = pipe_filter_to_command(wmic_process_list_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=MEDIUM_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_process_get(properties: Optional[List[str]] = None,
                     find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    wmic_process_get_command = WMIC_PROCESS_GET_COMMAND
    if properties:
        wmic_process_get_command += ", ".join(properties)
    full_command = pipe_filter_to_command(wmic_process_get_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=MEDIUM_TIMEOUT)


def get_parent_process_id(child_pid: int) -> Optional[int]:
    ppid_command = f"wmic process where (ProcessId={child_pid}) get ParentProcessId"
    output = CMD.execute_command_simply(ppid_command, timeout=SHORT_TIMEOUT)
    try:
        ppid_title, ppid = output.output_options.stdout_clean_lines
        return int(ppid)
    except ValueError:
        return None


def get_task_list_line_by_pid(pid: int) -> Optional[str]:
    output = task_list(find_str_filter=RegexFindStrFilter(f'^[^,]*,"{pid}"'))
    task_list_line = output.output_options.stdout_clean
    if NEW_LINE in task_list_line:
        return None
    return task_list_line


def get_wmic_brief_process_line_by_pid(pid: int) -> Optional[str]:
    output = wmic_process_brief_list(find_str_filter=RegexFindStrFilter(f'^.*,.*,.*,.*,{pid},.*,.*$'))
    wmic_brief_process_line = output.output_options.stdout_clean
    if NEW_LINE in wmic_brief_process_line:
        return None
    return wmic_brief_process_line

