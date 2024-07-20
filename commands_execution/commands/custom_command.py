from typing import Union, List, Optional, Dict, Any
from commands_execution.commands.command import Command


class CustomCommand(Command):
    def __init__(self, command: Union[str, List[str]], **custom_run_arguments):
        super().__init__(command=command)
        self.custom_run_arguments = custom_run_arguments

    @property
    def str_custom_run_arguments(self) -> str:
        return " & ".join([f"{key} = {value}" for key, value in self.custom_run_arguments.items()])

    def get_run_arguments(self) -> Dict[str, Any]:
        arguments = super()._basic_run_arguments()
        arguments.update(self.custom_run_arguments)
        return arguments

    def __str__(self) -> str:
        if self.str_custom_run_arguments:
            return f"{type(self).__name__}({self.str_command}, {self.str_custom_run_arguments})"
        else:
            return f"{type(self).__name__}({self.str_command})"

