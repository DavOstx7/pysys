from commands_execution.executables.executable import Executable
from commands_execution.commands_structures.piped_commands_structure import PipedCommandsStructure


class ProcessablePipedCommands:
    def __init__(self, executable: Executable, piped_commands_structure: PipedCommandsStructure):
        self.executable = executable
        self.piped_commands_structure = piped_commands_structure

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.executable} - {self.piped_commands_structure})"
