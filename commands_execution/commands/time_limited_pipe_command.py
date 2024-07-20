from typing import Union, List, Dict, Any
from commands_execution.commands.piped_command import PipedCommand
from commands_execution.outputs.output import Output


class TimeLimitedPipedCommand(PipedCommand):
    def __init__(self, command: Union[str, List[str]], timeout: int):
        super().__init__(command=command)
        self.timeout = timeout

    @property
    def str_timeout(self) -> str:
        return str(self.timeout) + 's'

    def get_run_arguments_from_piping(self, last_command_output: Union[str, Output]) -> Dict[str, Any]:
        arguments = super().get_run_arguments_from_piping(last_command_output)
        arguments["timeout"] = self.timeout
        return arguments
