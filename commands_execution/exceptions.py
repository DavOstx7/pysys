class CommandPipeError(ValueError):
    pass


class CommandTimeoutError(TimeoutError):
    pass


class OutputDecodingError(UnicodeDecodeError):
    pass


class CommandBadArgument(TypeError):
    pass
