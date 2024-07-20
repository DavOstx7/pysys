SC_QUERY_COMMAND = "sc query"
SC_QUERY_EXTENDED_COMMAND = "sc queryex"
SC_QUERY_CONFIGURATION_COMMAND = "sc_query qc"

SC_KEY_TO_VALUE_IDENTIFIER = b':'
WMIC_SERVICE_LIST_BRIEF_COMMAND = "wmic service list brief /FORMAT:CSV"
WMIC_SERVICE_LIST_COMMAND = "wmic service list"
WMIC_SERVICE_GET_COMMAND = "wmic service get"

WMIC_SERVICE_LIST_BRIEF_CSV_FORMAT = "Node,ExitCode,Name,ProcessId,StartMode,State,Status"

SC_FILTER_OPTIONS = {
    "type": ["driver", "service", "userservice", "all"],
    "state": ["inactive", "all"],
    "bufsize": ["<number> - default=4096"],
    "ri": ["<number> - default=0"],
    "group": ["<string> - default=all groups"]
}
