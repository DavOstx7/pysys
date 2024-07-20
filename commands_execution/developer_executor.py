import subprocess

from typing import Optional, Union
from commands_execution.commands.command import Command
from commands_execution.commands_structures.base_commands_structure import BaseCommandsStructure
from commands_execution.processable.processable_command import ProcessableCommand
from commands_execution.processable.processable_piped_commands import ProcessablePipedCommands
from commands_execution.outputs.output import Output
from commands_execution.outputs.full_output import FullOutput
from commands_execution.exceptions import CommandTimeoutError, CommandBadArgument


class DeveloperExecutor:
    def execute_command(self, processable_command: ProcessableCommand,
                        is_full_output: Optional[bool] = False) -> Output:
        try:
            executable_run_args = processable_command.executable.get_run_arguments()
            command_run_args = processable_command.command.get_run_arguments()
            completed_process: subprocess.CompletedProcess = subprocess.run(**executable_run_args, **command_run_args)
            if is_full_output:
                return self._get_full_output_from_completed_process(completed_process, processable_command.command)
            else:
                return self._get_output_from_completed_process(completed_process)
        except subprocess.TimeoutExpired as timeout_error:
            raise CommandTimeoutError(f"{processable_command} -> {timeout_error}") from timeout_error
        except TypeError as type_error:
            raise CommandBadArgument(f"{processable_command} -> {type_error}")from type_error

    def execute_piped_commands(self, processable_piped_commands: ProcessablePipedCommands,
                               is_full_output: Optional[bool] = False) -> Output:

        try:
            executable_run_args = processable_piped_commands.executable.get_run_arguments()
            first_command = processable_piped_commands.piped_commands_structure.first_command
            *piped_commands, last_piped_command = processable_piped_commands.piped_commands_structure.piped_commands
            last_command_output = subprocess.run(**first_command.get_run_arguments(), **executable_run_args).stdout
            for piped_command in piped_commands:
                piped_command_run_args = piped_command.get_run_arguments_from_piping(last_command_output)
                last_command_output = subprocess.run(**piped_command_run_args, **executable_run_args).stdout
            last_piped_command_run_args = last_piped_command.get_run_arguments_from_piping(last_command_output)
            completed_process: subprocess.CompletedProcess = subprocess.run(**executable_run_args,
                                                                            **last_piped_command_run_args)
            if is_full_output:
                return self._get_full_output_from_completed_process(completed_process,
                                                                    processable_piped_commands.piped_commands_structure)
            else:
                return self._get_output_from_completed_process(completed_process)
        except subprocess.TimeoutExpired as timeout_error:
            raise CommandTimeoutError(f"{processable_piped_commands} -> {timeout_error}") from timeout_error
        except TypeError as type_error:
            raise CommandBadArgument(f"{processable_piped_commands} -> {type_error}")from type_error

    @staticmethod
    def _get_output_from_completed_process(completed_process: subprocess.CompletedProcess) -> Output:
        output = Output(stdout=completed_process.stdout, stderr=completed_process.stderr,
                        exit_code=completed_process.returncode)
        return output

    @staticmethod
    def _get_full_output_from_completed_process(completed_process: subprocess.CompletedProcess,
                                                source_cause: Union[Command, BaseCommandsStructure]) -> FullOutput:
        full_output = FullOutput(source_cause=source_cause, stdout=completed_process.stdout,
                                 stderr=completed_process.stderr,
                                 exit_code=completed_process.returncode)
        return full_output
