from typing import Optional, List
from commands_execution import Executor, Output
from commands_execution.exceptions import CommandTimeoutError
from platform_independent.shared.utils import pipe_filter_to_command, retry
from platform_independent.shared.utils import append_filter_to_command
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from windows.variables_packing.sc.sc_query_filter import ScQueryFilter
from windows.consts import SHORT_TIMEOUT, MEDIUM_TIMEOUT, LONG_TIMEOUT
from windows.local.svcs.consts import SC_QUERY_COMMAND, SC_QUERY_EXTENDED_COMMAND, SC_QUERY_CONFIGURATION_COMMAND
from windows.local.svcs.consts import WMIC_SERVICE_LIST_BRIEF_COMMAND
from windows.local.svcs.consts import WMIC_SERVICE_GET_COMMAND, WMIC_SERVICE_LIST_COMMAND

CMD = Executor()


@retry(times=1, exceptions={CommandTimeoutError})
def sc_service_query(sc_filter: Optional[ScQueryFilter] = None,
                     find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    sc_query_command = append_filter_to_command(SC_QUERY_COMMAND, sc_filter)
    full_command = pipe_filter_to_command(sc_query_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=SHORT_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def sc_service_extended_query(sc_filter: Optional[ScQueryFilter] = None,
                              find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    sc_query_ex_command = append_filter_to_command(SC_QUERY_EXTENDED_COMMAND, sc_filter)
    full_command = pipe_filter_to_command(sc_query_ex_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=LONG_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def sc_service_configuration_query(service_name: str, sc_filter: Optional[ScQueryFilter] = None,
                                   find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    sc_query_qc_command = append_filter_to_command(SC_QUERY_CONFIGURATION_COMMAND, sc_filter,
                                                   in_between=service_name)
    full_command = pipe_filter_to_command(sc_query_qc_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=LONG_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_service_brief_list(find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    full_command = pipe_filter_to_command(WMIC_SERVICE_LIST_BRIEF_COMMAND, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=SHORT_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_service_list(find_str_filter: Optional[BaseFindStrFilter], list_format: Optional[str] = None):
    wmic_service_list_command = WMIC_SERVICE_LIST_COMMAND
    if list_format:
        wmic_service_list_command += f" {list_format}"
    full_command = pipe_filter_to_command(wmic_service_list_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=MEDIUM_TIMEOUT)


@retry(times=1, exceptions={CommandTimeoutError})
def wmic_service_get(properties: Optional[List[str]] = None,
                     find_str_filter: Optional[BaseFindStrFilter] = None) -> Output:
    wmic_service_get_command = WMIC_SERVICE_GET_COMMAND
    if properties:
        wmic_service_get_command += ", ".join(properties)
    full_command = pipe_filter_to_command(wmic_service_get_command, find_str_filter)
    return CMD.execute_command_simply(full_command, timeout=MEDIUM_TIMEOUT)
