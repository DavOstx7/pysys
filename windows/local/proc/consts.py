NON_ZIPPED_LINES_KEY = -1

TASK_LIST_CSV_FORMAT = '"Image Name","PID","Session Name","Session#","Mem Usage"'
WMIC_PROCESS_LIST_BRIEF_CSV_FORMAT = "Node,HandleCount,Name,Priority,ProcessId,ThreadCount,WorkingSetSize"

TASK_LIST_VALUES_REGEX = r'"(.*?)"'
TASK_LIST_PID_REGEX = r'^".*?","(\d+)"'

TASK_LIST_COMMAND = "tasklist /FO:CSV"
WMIC_PROCESS_LIST_BRIEF_COMMAND = "wmic process list brief /FORMAT:CSV"

WMIC_PROCESS_LIST_COMMAND = "wmic process list"

VERBOSE_TASK_LIST_COMMAND = "tasklist /V"
WMIC_PROCESS_GET_COMMAND = "wmic process get"

TASK_KILL_SUCCESS_IDENTIFIER = b"SUCCESS:"
WMIC_PROCESS_KILL_SUCCESS_IDENTIFIER = b"deletion successful."

TASK_KILL_ERROR_IDENTIFIER = b"ERROR:"
WMIC_PROCESS_KILL_ERROR_IDENTIFIER = b"ERROR:"

TASK_KILL_PROCESS_NOT_FOUND_IDENTIFIER = b"not found."
WMIC_PROCESS_KILL_NOT_FOUND_IDENTIFIER = b"No Instance"

TASK_LIST_WMIC_PROCESS_INFO_ATTRIBUTES = [
    "name", "pid", "session_name", "session_number", "mem_usage_kb", "node", "handle_count",
    "priority", "thread_count", "working_set_size_kb"
]

WMIC_PROCESS_GET_OPTIONS_LISTED = [
    "CSName", "CommandLine", "Description", "ExecutablePath", "ExecutionState",
    "Handle", "HandleCount", "InstallDate", "KernelModeTime", "MaximumWorkingSetSize", "MinimumWorkingSetSize",
    "Name", "OSName", "OtherOperationCount", "OtherTransferCount", "PageFaults", "PageFileUsage",
    "ParentProcessId", "PeakPageFileUsage", "PeakVirtualSize", "PeakWorkingSetSize", "Priority", "PrivatePageCount",
    "ProcessId", "QuotaNonPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
    "QuotaPeakPagedPoolUsage", "ReadOperationCount", "ReadTransferCount", "SessionId", "Status", "TerminationDate",
    "ThreadCount", "UserModeTime", "VirtualSize", "WindowsVersion", "WorkingSetSize",
    "WriteOperationCount", "WriteTransferCount"
]
