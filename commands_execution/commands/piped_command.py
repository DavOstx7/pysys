from typing import Union, List, Dict, Any
from commands_execution.commands.base.base_piped_command import BasePipedCommand
from commands_execution.commands.base.template_command import TemplateCommand
from commands_execution.outputs.output import Output


class PipedCommand(TemplateCommand, BasePipedCommand):
    def __init__(self, command: Union[str, List[str]]):
        super().__init__(command=command)

    def get_run_arguments_from_piping(self, last_command_output: Union[str, Output]) -> Dict[str, Any]:
        if isinstance(last_command_output, Output):
            last_command_output = last_command_output.stdout
        arguments = super()._basic_run_arguments()
        arguments["input"] = last_command_output
        return arguments
