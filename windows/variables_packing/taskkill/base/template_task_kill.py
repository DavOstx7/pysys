from abc import ABC
from windows.variables_packing.taskkill.base.base_task_kill import BaseTaskKill


class TemplateTaskKill(BaseTaskKill, ABC):
    def __init__(self, is_force: bool = False, is_include_childs: bool = False):
        self.is_force = is_force
        self.is_include_childs = is_include_childs

    def _basic_task_kill_command(self) -> str:
        task_kill_command = "taskkill "
        if self.is_force:
            task_kill_command += "/F "
        if self.is_include_childs:
            task_kill_command += "/T "
        return task_kill_command

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.get_task_kill_command()})"
