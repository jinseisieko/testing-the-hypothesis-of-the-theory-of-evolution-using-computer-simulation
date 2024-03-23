import time
import random

from .cell import DefaultCell, Cell, RedCell
import pygame as pg
from .const import RENDERING_ENHANCEMENT, FPS
from .debugging_data import time_decorator
import threading


class Field(object):
    def __init__(
            self,
            size: tuple[int, int],
            update_frequency: int = 30,
            render_frequency: int = FPS,
            default_cell=RedCell,
            borders=True,
    ) -> None:
        self.__size__ = size
        self.__default_cell__ = default_cell
        self.__borders__ = borders
        self.__update_frequency__ = update_frequency
        self.__render_frequency__ = render_frequency

        self.__render_size_cell__: int = int(100 * RENDERING_ENHANCEMENT)

        self.__cells__ = [
            [default_cell() for _ in range(size[0])] for _ in range(size[1])
        ]
        self.__need_render__ = [[True for _ in range(size[0])] for _ in range(size[1])]

        self.__surface__ = pg.Surface(
            (
                self.__size__[0] * self.__render_size_cell__,
                (self.__size__[1] * self.__render_size_cell__),
            )
        )

        self.__thread_update__ = threading.Thread(target=self.func_thread_update)
        self.__thread_render__ = threading.Thread(target=self.func_thread_render)

        self.__pause_update__ = False
        self.__pause_render__ = False
        self.__count_frames_update__ = 0

        self.__time_update__ = 1 / update_frequency
        self.__time_render__ = 1 / render_frequency

        self.event = Event()

    def func_thread_update(self):
        while True:
            start_time = time.time()
            if (not self.__pause_update__) or self.__count_frames_update__ > 0:
                self.update()
                if self.__count_frames_update__ > 0:
                    self.__count_frames_update__ -= 1
            end_time = time.time() - start_time
            if end_time < self.__time_update__:
                time.sleep(self.__time_update__ - end_time)

    def start_thread_update(self):
        self.__thread_update__.start()

    def func_thread_render(self):
        while True:
            start_time = time.time()
            if not self.__pause_render__:
                self.render()
            end_time = time.time() - start_time
            if end_time < self.__time_render__:
                time.sleep(self.__time_render__ - end_time)

    def start_thread_render(self):
        self.__thread_render__.start()

    def spawn_cell(self, x, y, class_, *args, **kwargs):
        self.__cells__[y][x] = class_(*args, **kwargs)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.__cells__[y][x]

    def get_pattern_cell(self, x: int, y: int) -> pg.Surface:
        return pg.transform.scale(
            self.get_cell(x, y).pattern,
            (self.__render_size_cell__, self.__render_size_cell__),
        )

    def draw_cell(self, x: int, y: int, pattern: pg.Surface) -> None:
        self.__surface__.blit(
            pattern, (x * self.__render_size_cell__, y * self.__render_size_cell__)
        )
        if self.__borders__:
            pg.draw.rect(
                self.__surface__,
                (0, 0, 0),
                (
                    x * self.__render_size_cell__,
                    y * self.__render_size_cell__,
                    self.__render_size_cell__,
                    self.__render_size_cell__,
                ),
                width=1,
            )

    @time_decorator(frequency=10)
    def render(self):
        for y in range(len(self.__need_render__)):
            for x in range(len(self.__need_render__[y])):
                if self.__need_render__[y][x]:
                    self.draw_cell(x, y, self.get_pattern_cell(x, y))
                    self.__need_render__[y][x] = False

    @time_decorator(frequency=10)
    def update(self):
        for y, line_cells in enumerate(self.__cells__):
            for x, cell in enumerate(line_cells):
                need_update = cell.update(self)
                if not (need_update is None) and not (self.__need_render__[y][x]):
                    self.__need_render__[y][x] = need_update


class Event:
    def __init__(self) -> None:
        self.__event_update__ = {}
        self.__event_render__ = {}
        self.__event_update_cell__ = {}
        self.__event_pause_update__ = {}
        self.__event_pause_render__ = {}
        self.__event_spawn_cell__ = {}
        self.__event_draw_cell__ = {}

    def event_update(self):
        for event in self.__event_update__.values():
            event()

    def add_event_update(self, event_name, event):
        self.__event_update__[event_name] = event

    def del_event_update(self, event_name):
        del self.__event_update__[event_name]

    def event_render(self, need_render):
        for event in self.__event_render__.values():
            event(need_render)

    def add_event_render(self, event_name, event):
        self.__event_render__[event_name] = event

    def del_event_render(self, event_name):
        del self.__event_render__[event_name]

    def event_update_cell(self, x, y):
        for event in self.__event_update_cell__.values():
            event(x, y)

    def add_event_update_cell(self, event_name, event):
        self.__event_update_cell__[event_name] = event

    def del_event_update_cell(self, event_name):
        del self.__event_update_cell__[event_name]

    def event_pause_update(self, pause):
        for event in self.__event_pause_update__.values():
            event(pause)

    def add_event_pause_update(self, event_name, event):
        self.__event_pause_update__[event_name] = event

    def del_event_pause_update(self, event_name):
        del self.__event_pause_update__[event_name]

    def event_pause_render(self, pause):
        for event in self.__event_pause_render__.values():
            event(pause)

    def add_event_pause_render(self, event_name, event):
        self.__event_pause_render__[event_name] = event

    def del_event_pause_render(self, event_name):
        del self.__event_pause_render__[event_name]

    def event_spawn_cell(self, x, y):
        for event in self.__event_spawn_cell__.values():
            event(x, y)

    def add_event_spawn_cell(self, event_name, event):
        self.__event_spawn_cell__[event_name] = event

    def del_event_spawn_cell(self, event_name):
        del self.__event_spawn_cell__[event_name]

    def event_draw_cell(self, x, y):
        for event in self.__event_draw_cell__.values():
            event(x, y)

    def add_event_draw_cell(self, event_name, event):
        self.__event_draw_cell__[event_name] = event

    def del_event_draw_cell(self, event_name):
        del self.__event_draw_cell__[event_name]
