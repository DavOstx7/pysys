from platform_independent.processes.base.base_processes_operations import BaseProcessesOperations

from typing import Callable, Union, List, Any
from platform_independent.processes.base.base_processes_info import BaseWindowsProcessesInfo
from platform_independent.processes.base import base_process_info
from windows.local.proc.process import Process
from windows.local.proc.consts import TASK_KILL_SUCCESS_IDENTIFIER, WMIC_PROCESS_KILL_SUCCESS_IDENTIFIER
from windows.local.proc.consts import TASK_KILL_PROCESS_NOT_FOUND_IDENTIFIER
from windows.local.proc.consts import WMIC_PROCESS_KILL_NOT_FOUND_IDENTIFIER
from windows.local.proc.consts import TASK_KILL_ERROR_IDENTIFIER, WMIC_PROCESS_KILL_ERROR_IDENTIFIER

from platform_independent.processes.exceptions import FunctionBadArgumentError, UnknownOutputError
from commands_execution import Output


class ProcessesOperations(BaseProcessesOperations):
    def __init__(self, processes_info: BaseWindowsProcessesInfo):
        self.processes = [Process(process_info) for process_info in processes_info]

    def _base_kill_processes_by_attribute(self, attribute: str, filter_function: Callable[[Union[str, int]], bool],
                                          result_function: Callable[[Output, Process], None],
                                          kill_function: Callable[[object, Any], Output],
                                          *kill_args, **kill_kwargs) -> Output:
        try:
            processes_to_kill = [process for process in self.processes if
                                 filter_function(getattr(process.process_info, attribute))]
        except AttributeError:
            raise AttributeError("The attribute given does not exist! Check the attribute list of the class used")
        except TypeError as type_error:
            raise FunctionBadArgumentError(
                "The filter_function should receive one argument (str or int) and return bool") from type_error
        else:
            kill_result_list = []
            for process in processes_to_kill:
                result = kill_function(process, *kill_args, **kill_kwargs)
                result_function(result, process)
                kill_result_list.append(result)
            return kill_result_list

    def kill_processes_by_attribute_using_task_kill(self, attribute: str,
                                                    filter_function: Callable[[Union[str, int]], bool],
                                                    is_force: bool = False, is_include_childs: bool = False) -> \
            List[Output]:
        return self._base_kill_processes_by_attribute(
            attribute=attribute,
            filter_function=filter_function,
            result_function=self.__task_kill_result_function,
            kill_function=Process.kill_process_using_task_kill,
            is_force=is_force, is_include_childs=is_include_childs
        )

    def kill_processes_by_attribute_using_wmic(self, attribute: str,
                                               filter_function: Callable[[Union[str, int]], bool],
                                               is_use_terminate_instead_of_delete: bool = False) -> \
            List[Output]:
        return self._base_kill_processes_by_attribute(
            attribute=attribute,
            filter_function=filter_function,
            result_function=self.__wmic_kill_result_function,
            kill_function=Process.kill_process_by_pid_using_wmic,
            is_use_terminate_instead_of_delete=is_use_terminate_instead_of_delete
        )

    def kill_all_processes(self) -> List[Output]:
        return self.kill_processes_by_pid(lambda pid: True)

    def kill_processes_by_attribute(self, attribute: str,
                                    filter_function: Callable[[Union[str, int]], bool]) -> List[Output]:
        return self.kill_processes_by_attribute_using_task_kill(attribute, filter_function)

    def kill_processes_by_name(self, filter_function: Callable[[str], bool]) -> List[Output]:
        return self.kill_processes_by_attribute(base_process_info.NAME_ATTRIBUTE_STR, filter_function)

    def kill_processes_by_pid(self, filter_function: Callable[[int], bool]) -> List[Output]:
        return self.kill_processes_by_attribute(base_process_info.PID_ATTRIBUTE_INT, filter_function)

    def __task_kill_result_function(self, result: Output, process: Process) -> None:
        if TASK_KILL_SUCCESS_IDENTIFIER in result.stdout:
            # Process removed successfully
            self.processes.remove(process)
        elif TASK_KILL_PROCESS_NOT_FOUND_IDENTIFIER in result.stderr:
            # Process is not found! removing a dead process
            self.processes.remove(process)
        elif TASK_KILL_ERROR_IDENTIFIER in result.stderr:
            pass
        else:
            raise UnknownOutputError(f"Cannot identify what happened: {result.stdout}, {result.stderr}")

    def __wmic_kill_result_function(self, result: Output, process: Process) -> None:
        if WMIC_PROCESS_KILL_SUCCESS_IDENTIFIER in result.stdout:
            # Process removed successfully
            self.processes.remove(process)
        elif WMIC_PROCESS_KILL_NOT_FOUND_IDENTIFIER in result.stdout:
            # Process is not found! removing a dead process
            self.processes.remove(process)
        elif WMIC_PROCESS_KILL_ERROR_IDENTIFIER in result.stderr:
            pass
        else:
            raise UnknownOutputError(f"Cannot identify what happened: {result.stdout}, {result.stderr}")
