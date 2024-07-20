import subprocess
from typing import Union, List, Dict, Any


class TemplateCommand:
    def __init__(self, command: Union[str, List[str]]):
        self.command = command

    @property
    def str_command(self) -> str:
        if type(self.command) == str:
            return self.command
        return " ".join(self.command)

    def _basic_run_arguments(self) -> Dict[str, Any]:
        return {"args": self.command, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE}

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.command})"
