from typing import Union, List, Optional, Dict, Any
from commands_execution.commands.command import Command


class TimeLimitedCommand(Command):
    def __init__(self, command: Union[str, List[str]], timeout: int, stdin: Optional[str] = None):
        super().__init__(command=command, stdin=stdin)
        self.timeout = timeout

    @property
    def str_timeout(self) -> str:
        return str(self.timeout) + 's'

    def get_run_arguments(self) -> Dict[str, Any]:
        arguments = super().get_run_arguments()
        arguments["timeout"] = self.timeout
        return arguments

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.str_command}, {self.str_timeout})"
