import subprocess

from typing import Optional, Union, List
from commands_execution.executables.known_executables import DEFAULT_EXECUTABLE
from commands_execution.executables.executable import Executable
from commands_execution.outputs.output import Output
from commands_execution.commands.command import Command
from commands_execution.commands.time_limited_command import TimeLimitedCommand
from commands_execution.commands.piped_command import PipedCommand
from commands_execution.commands.time_limited_pipe_command import TimeLimitedPipedCommand
from commands_execution.processable.processable_command import ProcessableCommand
from commands_execution.commands_structures.piped_commands_structure import PipedCommandsStructure
from commands_execution.processable.processable_piped_commands import ProcessablePipedCommands
from commands_execution.developer_executor import DeveloperExecutor

SUBPROCESSModule = type(subprocess)


# Should I use in the signature -> Output (scalable, but not good for typing - will need manually a type) or:
# 1) Make separate functions with one having Output and the other having FullOutput - a lot of functions
# 2) Return a union of [Output, FullOutput] - If a new type of output is available, it will need a change

class Executor(DeveloperExecutor):
    def __init__(self, default_executable: Optional[Union[str, Executable]] = None):
        if default_executable is None:
            self.__default_executable = DEFAULT_EXECUTABLE
        elif type(default_executable) == str:
            self.__default_executable = Executable(path=default_executable)
        elif isinstance(default_executable, Executable) == Executable:
            self.__default_executable = default_executable
        else:
            raise TypeError(f"The given default_executable should not be of type {type(default_executable)}")

    @property
    def subprocess_module(self) -> SUBPROCESSModule:
        return subprocess

    def set_default_executable(self, default_executable: Union[str, Executable]) -> None:
        if type(default_executable) == str:
            self.__default_executable = Executable(path=default_executable)
        elif isinstance(default_executable, Executable):
            self.__default_executable = default_executable
        else:
            raise TypeError(f"The given default_executable should not be of type {type(default_executable)}")

    def execute_command_simply(self, simple_command: Union[str, List[str]],
                               stdin: Optional[str] = None,
                               timeout: Optional[int] = None,
                               is_full_output: Optional[bool] = False) -> Output:

        processable_command = ProcessableCommand(
            executable=self.__default_executable,
            command=self.get_corresponding_command(simple_command, stdin=stdin, timeout=timeout)
        )
        return self.execute_command(processable_command, is_full_output)

    def execute_piped_commands_simply(self, simple_command: Union[str, List[str]],
                                      simple_piped_commands: List[Union[str, List[str]]],
                                      timeout_per_command: Optional[int],
                                      simple_command_stdin: Optional[str] = None,
                                      is_full_output: Optional[bool] = False) -> Output:

        piped_commands_structure = PipedCommandsStructure(
            first_command=self.get_corresponding_command(simple_command, stdin=simple_command_stdin,
                                                         timeout=timeout_per_command),
            piped_commands=[self.get_corresponding_piped_command(piped_command, timeout=timeout_per_command)
                            for piped_command in simple_piped_commands]
        )
        processable_piped_commands = ProcessablePipedCommands(
            executable=self.__default_executable,
            piped_commands_structure=piped_commands_structure
        )
        return self.execute_piped_commands(processable_piped_commands, is_full_output)

    @staticmethod
    def get_corresponding_command(simple_command, stdin: Optional[str] = None, timeout: Optional[int] = None) \
            -> Union[Command, TimeLimitedCommand]:
        if timeout is not None:
            return TimeLimitedCommand(simple_command, stdin=stdin, timeout=timeout)
        else:
            return Command(simple_command, stdin=stdin)

    @staticmethod
    def get_corresponding_piped_command(simple_piped_command, timeout: Optional[int] = None) \
            -> Union[PipedCommand, TimeLimitedPipedCommand]:
        if timeout is not None:
            return TimeLimitedPipedCommand(simple_piped_command, timeout=timeout)
        else:
            return PipedCommand(simple_piped_command)
