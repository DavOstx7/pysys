import re
from typing import Optional, List, Union, Tuple, Dict
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from windows.local.proc.utils import process_info_utils
from windows.consts import FIRST_LINE_INDEX, ONE_LINE, TWO_LINES
from platform_independent.processes.exceptions import TaskListFormatError, WmicProcessBriefListFormatError
from platform_independent.processes.exceptions import ZippedTaskListWmicError
from windows.local.proc.consts import TASK_LIST_CSV_FORMAT, TASK_LIST_VALUES_REGEX
from windows.local.proc.consts import WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT, NON_ZIPPED_LINES_KEY


def get_task_list_lines(find_str_filter: Optional[BaseFindStrFilter] = None) -> List[str]:
    task_list_output = process_info_utils.task_list(find_str_filter)
    task_list_output_lines = task_list_output.output_options.stdout_clean_lines
    if len(task_list_output_lines) > ONE_LINE and task_list_output_lines[FIRST_LINE_INDEX] == TASK_LIST_CSV_FORMAT:
        return task_list_output_lines[FIRST_LINE_INDEX + ONE_LINE:]
    else:
        return task_list_output_lines


def get_wmic_brief_processes_lines(find_str_filter: Optional[BaseFindStrFilter] = None) -> List[str]:
    wmic_brief_processes_output = process_info_utils.wmic_process_brief_list(find_str_filter)
    wmic_brief_processes_output_lines = wmic_brief_processes_output.output_options.stdout_clean_lines
    if (len(wmic_brief_processes_output_lines) > ONE_LINE
            and wmic_brief_processes_output_lines[FIRST_LINE_INDEX] == WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT):
        return wmic_brief_processes_output_lines[FIRST_LINE_INDEX + ONE_LINE:]
    else:
        return wmic_brief_processes_output_lines


def parse_task_list_line(task_list_line: Union[str, bytes]) -> Tuple[str, int, str, int, int]:
    if type(task_list_line) == bytes:
        task_list_line = task_list_line.decode()
    try:
        task_list_values = re.findall(TASK_LIST_VALUES_REGEX, task_list_line)
        image_name, pid, session_name, session_number, mem_usage = task_list_values
        pid = int(pid)
        session_number = int(session_number)
        mem_usage, kb_unit_type = mem_usage.split()
        mem_usage_kb = int(mem_usage.replace(',', ''))

    except ValueError as value_error:
        raise TaskListFormatError(
            f"The given format for the task list line is incorrect! follow this format: {TASK_LIST_CSV_FORMAT}"
        ) from value_error
    else:
        return image_name, pid, session_name, session_number, mem_usage_kb


def parse_wmic_brief_process_line(wmic_brief_process_line: Union[str, bytes]) \
        -> Tuple[str, int, str, int, int, int, int]:
    if type(wmic_brief_process_line) == bytes:
        wmic_brief_process_line = wmic_brief_process_line.decode()
    try:
        wmic_brief_process_values = wmic_brief_process_line.split(',')
        node, handle_count, name, priority, process_id, thread_count, working_set_size = wmic_brief_process_values

        handle_count = int(handle_count)
        priority = int(priority)
        process_id = int(process_id)
        thread_count = int(thread_count)
        working_set_size_kb = int(working_set_size)

    except ValueError as value_error:
        raise WmicProcessBriefListFormatError(
            f"The given format for the task list line is incorrect! follow this format:"
            f" {WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT}"
        ) from value_error
    else:
        return node, handle_count, name, priority, process_id, thread_count, working_set_size_kb


def parse_pid_from_task_list_line(task_list_line: Union[str, bytes]) -> int:
    _, pid, _, _, _ = parse_task_list_line(task_list_line)
    return pid


def parse_pid_from_wmic_brief_processes_line(wmic_brief_process_line: Union[str, bytes]) -> int:
    _, _, _, _, process_id, _, _ = parse_wmic_brief_process_line(wmic_brief_process_line)
    return process_id


def get_parsed_task_list_line_by_pid(pid: int):
    return parse_task_list_line(process_info_utils.get_task_list_line_by_pid(pid))


def get_parsed_wmic_brief_process_line_by_pid(pid: int):
    return parse_wmic_brief_process_line(
        process_info_utils.get_wmic_brief_process_line_by_pid(pid)
    )


def get_zipped_matching_task_list_and_wmic_brief_lines(find_str_filter: Optional[BaseFindStrFilter] = None) -> \
        Dict[int, List[str]]:
    task_list_lines = get_task_list_lines(find_str_filter)
    wmic_brief_processes_lines = get_wmic_brief_processes_lines(find_str_filter)
    pid_to_matching_lines_mapper: Dict[int, List[str]] = {NON_ZIPPED_LINES_KEY: []}

    for task_list_line in task_list_lines:
        task_list_pid = parse_pid_from_task_list_line(task_list_line)
        if task_list_pid in pid_to_matching_lines_mapper:
            pid_to_matching_lines_mapper[task_list_pid].append(task_list_line)
        else:
            pid_to_matching_lines_mapper[task_list_pid] = [task_list_line]

    for wmic_brief_process_line in wmic_brief_processes_lines:
        wmic_brief_process_pid = parse_pid_from_wmic_brief_processes_line(wmic_brief_process_line)
        if wmic_brief_process_pid in pid_to_matching_lines_mapper:
            pid_to_matching_lines_mapper[wmic_brief_process_pid].append(wmic_brief_process_line)
        else:
            pid_to_matching_lines_mapper[wmic_brief_process_pid] = [wmic_brief_process_line]

    for pid, lines in list(pid_to_matching_lines_mapper.items()):
        if len(lines) == ONE_LINE:
            pid_to_matching_lines_mapper[NON_ZIPPED_LINES_KEY].extend(lines)
            del pid_to_matching_lines_mapper[pid]
        elif len(lines) > TWO_LINES:
            raise ZippedTaskListWmicError("3 lines occurred when zipping by pid from 2 sources")

    return pid_to_matching_lines_mapper
