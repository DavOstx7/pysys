from typing import Union, List, Optional, Dict, Any
from commands_execution.commands.base.base_command import BaseCommand
from commands_execution.commands.base.template_command import TemplateCommand


class Command(TemplateCommand, BaseCommand):
    def __init__(self, command: Union[str, List[str]], stdin: Optional[str] = None):
        super().__init__(command=command)
        self.stdin = stdin

    def get_run_arguments(self) -> Dict[str, Any]:
        arguments = super()._basic_run_arguments()
        arguments["input"] = self.stdin
        return arguments
