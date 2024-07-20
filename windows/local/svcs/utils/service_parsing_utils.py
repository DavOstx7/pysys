from typing import Optional, List, Tuple, Union
from commands_execution import Output
from platform_independent.shared.enum_info import EnumInfo
from windows.variables_packing.findstr.base.base_findstr_filter import BaseFindStrFilter
from windows.local.svcs.utils import service_info_utils
from windows.consts import FIRST_LINE_INDEX, ONE_LINE, EMPTY_BYTES_LINE
from windows.consts import SECOND_ELEMENT_INDEX, HEXADECIMAL_BASE
from windows.local.svcs.consts import WMIC_SERVICE_LIST_BRIEF_CSV_FORMAT, SC_KEY_TO_VALUE_IDENTIFIER
from windows.variables_packing.sc.sc_query_filter import ScQueryFilter
from platform_independent.services.exceptions import WmicServiceBriefListFormatError, ScServiceQueryFormatError
from platform_independent.services.exceptions import ScServiceQueryExFormatError


def fix_line(line: str) -> str:
    return ' '.join(line.strip().split())


def divided_sc_lists(sc_output: Output) -> List[List[str]]:
    output_lines = sc_output.output_options.stdout_lines
    if len(output_lines) > ONE_LINE and output_lines[FIRST_LINE_INDEX] == EMPTY_BYTES_LINE:
        output_lines = output_lines[FIRST_LINE_INDEX + ONE_LINE:]
    services_lines: List[List[str]] = []
    service_lines: List[str] = []
    for service_line in output_lines:
        if service_line:
            if SC_KEY_TO_VALUE_IDENTIFIER in service_line:
                service_lines.append(fix_line(service_line.decode()))
        else:
            services_lines.append(service_lines)
            service_lines = []
    return services_lines


def get_sc_services_query_lists(sc_filter: Optional[ScQueryFilter] = None) -> List[List[str]]:
    sc_query_output = service_info_utils.sc_service_query(sc_filter=sc_filter)
    return divided_sc_lists(sc_query_output)


def get_sc_services_query_extended_lists(sc_filter: Optional[ScQueryFilter] = None) -> List[List[str]]:
    sc_query_extended_output = service_info_utils.sc_service_extended_query(sc_filter=sc_filter)
    return divided_sc_lists(sc_query_extended_output)


def get_wmic_brief_services_lines(find_str_filter: Optional[BaseFindStrFilter] = None) -> List[str]:
    if find_str_filter:
        wmic_brief_services_output = service_info_utils.wmic_service_brief_list(find_str_filter)
    else:
        wmic_brief_services_output = service_info_utils.wmic_service_brief_list()
    wmic_brief_services_output_lines = wmic_brief_services_output.output_options.stdout_clean_lines
    if (len(wmic_brief_services_output_lines) > ONE_LINE
            and wmic_brief_services_output_lines[FIRST_LINE_INDEX] == WMIC_SERVICE_LIST_BRIEF_CSV_FORMAT):
        return wmic_brief_services_output_lines[FIRST_LINE_INDEX + ONE_LINE:]
    else:
        return wmic_brief_services_output_lines


def parse_sc_query_lines(sc_query_lines: List[str]) -> Tuple[str, str, EnumInfo, EnumInfo, int, int, int, int]:
    sc_query_values = [sc_query_line.split(SC_KEY_TO_VALUE_IDENTIFIER.decode())[SECOND_ELEMENT_INDEX].strip()
                       for sc_query_line in sc_query_lines]
    try:
        service_name, display_name, service_type, state = sc_query_values[:-4]
        win32_exit_code, service_exit_code, check_point, wait_hint = sc_query_values[-4:]

        service_type, state = EnumInfo(service_type), EnumInfo(state)
        win32_exit_code_int, win32_exit_code_hex = win32_exit_code.split()
        service_exit_code_int, service_exit_code_hex = service_exit_code.split()
        win32_exit_code, service_exit_code = int(win32_exit_code_int), int(service_exit_code_int)
        check_point, wait_hint = int(check_point, HEXADECIMAL_BASE), int(wait_hint, HEXADECIMAL_BASE)
    except ValueError as value_error:
        raise ScServiceQueryFormatError(f"The given format for the sc query service is incorrect!") from value_error
    else:
        return (
            service_name, display_name, service_type, state, win32_exit_code, service_exit_code, check_point, wait_hint
        )


def parse_sc_query_extended_lines(sc_query_extended_lines: List[str]) -> \
        Tuple[str, str, EnumInfo, EnumInfo, int, int, int, int, int, str]:
    sc_query_lines, sc_query_extension_lines = sc_query_extended_lines[:-2], sc_query_extended_lines[-2:]
    sc_query_extension_values = [
        sc_query_extension.split(SC_KEY_TO_VALUE_IDENTIFIER.decode())[SECOND_ELEMENT_INDEX].strip()
        for sc_query_extension in sc_query_extension_lines
    ]
    try:
        pid, flags = sc_query_extension_values
        pid = int(pid)
        full_parsed_values = parse_sc_query_lines(sc_query_lines) + (pid, flags)
    except ValueError as value_error:
        raise ScServiceQueryExFormatError(f"The given format for the sc queryex service is incorrect!") from value_error
    else:
        return full_parsed_values


def parse_wmic_brief_services_line(wmic_brief_service_line: Union[str, bytes]) -> \
        Tuple[str, int, str, int, str, str, str]:
    if type(wmic_brief_service_line) == bytes:
        wmic_brief_service_line = wmic_brief_service_line.decode()
    wmic_brief_service_values = wmic_brief_service_line.split(',')
    try:
        node, exit_code, name, process_id, start_mode, state, status = wmic_brief_service_values

        exit_code = int(exit_code)
        process_id = int(process_id)
    except ValueError as value_error:
        raise WmicServiceBriefListFormatError(
            f"The given format for the task list line is incorrect! follow this format:"
            f" {WMIC_SERVICE_LIST_BRIEF_CSV_FORMAT}"
        ) from value_error
    else:
        return node, exit_code, name, process_id, start_mode, state, status
