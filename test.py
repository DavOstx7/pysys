"""
returns the correct format for creating ProcessInfo list.
"""
from typing import Union, List

SEPARATOR_LINE_INDEX = 1
EMPTY_LENGTH = 0


class ProcessUtils:
    @staticmethod
    def correct_tasks_line_separator_start(line: Union[str, bytes]) -> Union[str, bytes]:
        return "=====" if type(line) == str else b"====="

    @staticmethod
    def clean_tasklist_lines(tasklist_lines: Union[str, bytes, List[Union[str, bytes]]]):
        if type(tasklist_lines) != list:
            tasklist_lines = tasklist_lines.strip().splitlines()
        tasklist_lines = [line.strip() for line in tasklist_lines if line.strip()]
        if len(tasklist_lines) == EMPTY_LENGTH:
            return []
        tasks_line_separator_start = ProcessUtils.correct_tasks_line_separator_start(
            tasklist_lines[SEPARATOR_LINE_INDEX]
        )
        found_separator_index = None
        for index, line in enumerate(tasklist_lines, 0):
            if line.startswith(tasks_line_separator_start):
                found_separator_index = index
        if found_separator_index != None:
            # Python does not throw an error for using bad index on the index slicing, but logically it needs to be.
            if not (found_separator_index + 1 < len(tasklist_lines)):
                return []
            tasklist_lines = tasklist_lines[found_separator_index + 1:]
        return tasklist_lines

# [ProcessInfo(tasklist_line) for tasklist_line in tasklist_lines]
