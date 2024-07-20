from platform_independent.processes.base.base_process_info import BaseWindowsProcessInfo


class UnknownProcessInfo(BaseWindowsProcessInfo):
    def get_parent_process_info(self):
        return None
