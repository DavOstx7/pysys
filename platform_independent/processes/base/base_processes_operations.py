from abc import ABC, abstractmethod
from typing import List, Callable, Union
from commands_execution import Output


class BaseProcessesOperations(ABC):
    @abstractmethod
    def kill_processes_by_attribute(self, attribute: str, filter_function: Callable[[Union[str, int]], bool]) \
            -> List[Output]:
        pass

