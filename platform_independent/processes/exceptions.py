class TaskListFormatError(SyntaxError):
    pass


class WmicProcessBriefListFormatError(SyntaxError):
    pass


class FunctionBadArgumentError(TypeError):
    pass


class UnknownOutputError(Exception):
    pass


class ZippedTaskListWmicError(Exception):
    pass


class EmptyProcesses(ValueError):
    pass
