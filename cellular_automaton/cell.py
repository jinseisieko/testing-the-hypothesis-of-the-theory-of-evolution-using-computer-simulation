from abc import ABC, abstractmethod
import random
import pygame as pg


class Cell(ABC):
    def __init__(self) -> None: ...

    @abstractmethod
    def update(self, field) -> bool: ...

    @property
    @abstractmethod
    def pattern(self) -> pg.Surface: ...


class DefaultCell(Cell):
    def __init__(self) -> None:
        super().__init__()

        self.appear = False

    @property
    def pattern(self) -> pg.Surface:
        default_surface = pg.Surface((100, 100))
        default_surface.fill((255, 255, 255))
        return default_surface

    def update(self, _):
        if not self.appear:
            self.appear = True
            return True
        return False


class RedCell(Cell):
    @property
    def pattern(self) -> pg.Surface:
        surface = pg.Surface((100, 100))
        surface.fill((min(self.value, 255), 0, 0))
        return surface

    def __init__(self):
        super().__init__()
        self.value = 10

    def update(self, _):
        if self.value > 255:
            self.value = 10 + random.randint(0, 20)
        self.value += random.randint(0, 1)
        if self.value % random.randint(1, 20) == 0:
            return True
        return False
