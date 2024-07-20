from typing import Dict, Any
from abc import ABC, abstractmethod


class BasePipedCommand(ABC):
    @abstractmethod
    def get_run_arguments_from_piping(self, last_command_output: str) -> Dict[str, Any]:
        pass
