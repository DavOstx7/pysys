from windows.variables_packing.taskkill.base.template_task_kill import TemplateTaskKill


class TaskKillByPid(TemplateTaskKill):
    def __init__(self, pid: int, is_force: bool = False, is_include_childs: bool = False):
        super().__init__(is_force=is_force, is_include_childs=is_include_childs)
        self.pid = pid

    def get_task_kill_command(self) -> str:
        task_kill_command = self._basic_task_kill_command()
        task_kill_command += f"/PID {self.pid}"
        return task_kill_command
