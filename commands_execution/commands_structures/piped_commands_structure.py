from typing import List

from commands_execution.commands.piped_command import PipedCommand
from commands_execution.commands.command import Command
from commands_execution.commands_structures.base_commands_structure import BaseCommandsStructure


class PipedCommandsStructure(BaseCommandsStructure):
    def __init__(self, first_command: Command, piped_commands: List[PipedCommand]):
        self.first_command = first_command
        self.piped_commands = piped_commands

    @property
    def str_commands_piping(self) -> str:
        return " | ".join(str(command) for command in [self.first_command, *self.piped_commands])

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.str_commands_piping})"
