from typing import Optional, Union, Dict
from pathlib2 import PurePath


class Executable:
    def __init__(self, path: Optional[Union[PurePath, str]] = None, is_run_in_shell: Optional[bool] = True,
                 name: Optional[str] = None):
        self.path = path
        self.is_run_in_shell = is_run_in_shell
        self.name = name

    @property
    def str_path(self) -> Optional[str]:
        if self.path:
            return str(self.path)

    def get_run_arguments(self) -> Dict:
        return {"executable": self.str_path, "shell": self.is_run_in_shell}

    def __str__(self) -> str:
        if self.name:
            executable = self.name
        else:
            if self.path:
                executable = self.path
            else:
                executable = "SystemDefault"
        return f"{type(self).__name__}({executable})"
