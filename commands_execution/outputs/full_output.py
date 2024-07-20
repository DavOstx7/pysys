from typing import Union, Optional
from commands_execution.commands.command import Command
from commands_execution.commands_structures.base_commands_structure import BaseCommandsStructure
from commands_execution.outputs.output import Output


class FullOutput(Output):
    def __init__(self, source_cause: Union[Command, BaseCommandsStructure], stdout: bytes, stderr: bytes,
                 exit_code: Optional[int] = None):
        super().__init__(stdout=stdout, stderr=stderr, exit_code=exit_code)
        self.source_cause = source_cause

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.source_cause} -> {type(self).__base__.__name__}({self.stdout}))"
