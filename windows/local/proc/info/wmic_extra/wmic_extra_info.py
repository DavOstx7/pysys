from typing import List, Optional
from commands_execution import Executor, Output
from windows.consts import SHORT_TIMEOUT, NEW_LINE
from windows.local.proc.consts import WMIC_PROCESS_GET_OPTIONS_LISTED
from windows.local.proc.utils import process_info_utils, process_parsing_utils
from platform_independent.shared.utils import parse_date_time_to_str, convert_100_nanoseconds_time_to_seconds_time
WMIC_PROCESS_GET_OPTIONS_LISTED: List[str] = WMIC_PROCESS_GET_OPTIONS_LISTED

CMD = Executor()


class WmicExtraInfo:
    def __init__(self, pid: int, is_constantly_update: bool = True):
        self.__pid = pid
        self.is_constantly_update = is_constantly_update
        self._description, self._command_line, self._executable_path, self._creation_date = None, None, None, None
        self._parent_pid, self._session_id = None, None
        self._user_mode_time_in_seconds, self._kernel_mode_time_in_seconds = None, None

    def get_wmic_attribute(self, attribute: str) -> Output:
        if hasattr(self, attribute):
            return getattr(self, attribute)

        custom_attribute_command = f"wmic process where (ProcessId={self.__pid}) get {attribute}"
        return CMD.execute_command_simply(custom_attribute_command, timeout=SHORT_TIMEOUT)

    # The attributes ExecutionState and Status are always NULL from what the docs and third-party say.

    @property
    def description(self) -> Optional[str]:
        if not self.is_constantly_update and self._description:
            return self._description

        description_command = f"wmic process where (ProcessId={self.__pid}) get Description"
        output = CMD.execute_command_simply(description_command, timeout=SHORT_TIMEOUT)
        try:
            description_title, *description = output.output_options.stdout_clean_lines
            description = NEW_LINE.join(description)
            self._description = description
            return description
        except ValueError:
            return None

    @property
    def command_line(self) -> Optional[str]:
        if not self.is_constantly_update and self._command_line:
            return self._command_line
        command_line_command = f"wmic process where (ProcessId={self.__pid}) get CommandLine"
        output = CMD.execute_command_simply(command_line_command, timeout=SHORT_TIMEOUT)
        try:
            command_line_title, self._command_line = output.output_options.stdout_clean_lines
            return self._command_line
        except ValueError:
            return None

    @property
    def executable_path(self) -> Optional[str]:
        if not self.is_constantly_update and self._executable_path:
            return self._executable_path
        executable_path_command = f"wmic process where (ProcessId={self.__pid}) get ExecutablePath"
        output = CMD.execute_command_simply(executable_path_command, timeout=SHORT_TIMEOUT)
        try:
            executable_path_title, self._executable_path = output.output_options.stdout_clean_lines
            return self._executable_path
        except ValueError:
            return None

    @property
    def creation_date(self) -> Optional[str]:
        if not self.is_constantly_update and self._creation_date:
            return self._creation_date
        creation_date_command = f"wmic process where (ProcessId={self.__pid}) get CreationDate"
        output = CMD.execute_command_simply(creation_date_command, timeout=SHORT_TIMEOUT)
        try:
            creation_date_title, creation_date = output.output_options.stdout_clean_lines
            self._creation_date = parse_date_time_to_str(creation_date)
            return self._creation_date
        except ValueError:
            return None

    @property
    def parent_pid(self) -> Optional[int]:
        if not self.is_constantly_update and self._parent_pid:
            return self._parent_pid
        self._parent_pid = process_info_utils.get_parent_process_id(self.__pid)
        return self._parent_pid

    @property
    def session_id(self) -> Optional[str]:
        if not self.is_constantly_update and self._session_id:
            return self._session_id
        session_id_command = f"wmic process where (ProcessId={self.__pid}) get SessionId"
        output = CMD.execute_command_simply(session_id_command, timeout=SHORT_TIMEOUT)
        try:
            session_id_title, session_id = output.output_options.stdout_clean_lines
            self._session_id = int(session_id)
            return self._session_id
        except ValueError:
            return None

    @property
    def user_mode_time_in_seconds(self) -> Optional[int]:
        if not self.is_constantly_update and self._user_mode_time_in_seconds:
            return self._user_mode_time_in_seconds
        user_mode_time_command = f"wmic process where (ProcessId={self.__pid}) get UserModeTime"
        output = CMD.execute_command_simply(user_mode_time_command, timeout=SHORT_TIMEOUT)
        try:
            user_mode_time_title, user_mode_time = output.output_options.stdout_clean_lines
            self._user_mode_time_in_seconds = convert_100_nanoseconds_time_to_seconds_time(int(user_mode_time))
            return self._user_mode_time_in_seconds
        except ValueError:
            return None

    @property
    def kernel_mode_time_in_seconds(self) -> Optional[int]:
        if not self.is_constantly_update and self._kernel_mode_time_in_seconds:
            return self._kernel_mode_time_in_seconds
        kernel_mode_time_command = f"wmic process where (ProcessId={self.__pid}) get KernelModeTime"
        output = CMD.execute_command_simply(kernel_mode_time_command, timeout=SHORT_TIMEOUT)
        try:
            kernel_mode_time_title, kernel_mode_time = output.output_options.stdout_clean_lines
            self._kernel_mode_time_in_seconds = convert_100_nanoseconds_time_to_seconds_time(int(kernel_mode_time))
            return self._kernel_mode_time_in_seconds
        except ValueError:
            return None

    def __str__(self) -> str:
        return f"{type(self).__name__}(PID = {self.__pid}, PPID = {self.parent_pid}, Path = {self.executable_path})"
