from abc import ABC, abstractmethod


class BaseTaskKill(ABC):
    @abstractmethod
    def get_task_kill_command(self) -> str:
        pass
