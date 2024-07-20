from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def get_run_arguments(self) -> Dict[str, Any]:
        pass
