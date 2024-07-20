from abc import ABC, abstractmethod
from commands_execution import Output


class BaseProcessOperations(ABC):
    @abstractmethod
    def kill_process(self) -> Output:
        pass
