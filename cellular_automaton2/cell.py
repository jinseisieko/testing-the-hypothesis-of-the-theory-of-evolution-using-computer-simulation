from abc import ABC, abstractmethod
from typing import Any


class Cell(ABC):
    def __init__(self, pattern_id: str, data: Any, *args, **kwargs) -> None:
        self.data: Any = data
        self.pattern_id: str = pattern_id

    @abstractmethod
    def update(self, field, information: dict) -> bool:
        raise NotImplementedError


class DefaultCell(Cell):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("white", None)

    def update(self, field, information: dict) -> bool:
        return False
