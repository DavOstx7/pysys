from abc import ABC, abstractmethod


class BaseCommandsStructure(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
