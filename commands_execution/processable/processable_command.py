from commands_execution.executables.executable import Executable
from commands_execution.commands.command import Command


class ProcessableCommand:
    def __init__(self, executable: Executable, command: Command):
        self.executable = executable
        self.command = command

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.executable} - {self.command})"
