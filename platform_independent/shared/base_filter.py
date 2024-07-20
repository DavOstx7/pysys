from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    def get_filter_command(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.get_filter_command()})"
