import copy
import time
import random
from pprint import pprint

from .Exceptions.field_Exceptions import SpawnCellException, GetCellException, GetPatternCellException, \
    DrawCellException
from .cell import DefaultCell, Cell, RedCell
import pygame as pg
from .const import RENDERING_ENHANCEMENT, FPS
from .debugging_data import time_decorator
import threading


class Field(object):
    """Class that implements the field and related functions"""

    def __init__(
            self,
            size: tuple[int, int],
            update_frequency: int = 30,
            render_frequency: int = FPS,
            default_cell: type = DefaultCell,
            borders: bool = True,
            layer_by_layer_update: bool = False,
            forced_rendering_of_all_pixels: bool = True,
    ) -> None:
        self.__size__: tuple[int, int] = size  # Field size in cells
        self.__default_cell__: type = default_cell  # All initial cells will be created of this class
        self.__borders__: bool = borders  # Will the boundaries of the cells be drawn
        self.__update_frequency__: int = update_frequency  # Cell renewal rate (fields)
        self.__render_frequency__: int = render_frequency  # Field rendering speed
        self.__layer_by_layer_update__: bool = layer_by_layer_update  # layer-by-layer update
        self.__forced_rendering_of_all_pixels__: bool = forced_rendering_of_all_pixels  # forced rendering of all pixels

        # cell size on the surface of this class
        self.__render_size_cell__: int = int(100 * RENDERING_ENHANCEMENT)

        # thread to regulate field update
        self.__thread_update__: threading.Thread = threading.Thread(target=self.func_thread_update)

        # thread to regulate render
        self.__thread_render__: threading.Thread = threading.Thread(target=self.func_thread_render)

        # pause to stop updates
        self.__pause_update__: bool = False

        # pause to stop render
        self.__pause_render__: bool = False

        # the number of frames that will load even with a pause
        self.__count_frames_update__: int = 0

        # time to be spent on one update
        self.__time_update__: float = 1 / update_frequency

        # time to be spent on one render
        self.__time_render__: float = 1 / render_frequency

        # object which is responsible for functions called at certain events
        self.event: Event = Event()

        # field
        self.__cells__: list = [
            [default_cell() for _ in range(size[0])] for _ in range(size[1])
        ]

        self.__next__cells__ = copy.deepcopy(self.__cells__)

        # array that is responsible for the need to render the cell
        self.__need_render__: list = [[True for _ in range(size[0])] for _ in range(size[1])]

        # main surface where the field is displayed
        self.__surface__: pg.Surface = pg.Surface(
            (
                self.__size__[0] * self.__render_size_cell__,
                (self.__size__[1] * self.__render_size_cell__),
            )
        )

    def func_thread_update(self):
        """update thread function"""
        while True:
            start_time = time.time()

            if (not self.__pause_update__) or self.__count_frames_update__ > 0:

                self.__update__()  # challenges of the update function

                if self.__count_frames_update__ > 0:
                    self.__count_frames_update__ -= 1

            end_time = time.time() - start_time
            if end_time < self.__time_update__:
                time.sleep(self.__time_update__ - end_time)

    def start_thread_update(self):
        """start update thread"""
        self.__thread_update__.start()

    def func_thread_render(self):
        """render thread function"""
        while True:
            start_time = time.time()

            if not self.__pause_render__:
                self.__render__()  # challenges of the render function

            end_time = time.time() - start_time
            if end_time < self.__time_render__:
                time.sleep(self.__time_render__ - end_time)

    def start_thread_render(self):
        """start render thread"""
        self.__thread_render__.start()

    def spawn_cell(self, x: int, y: int, class_, *args, **kwargs):
        """
        Spawn cell in specified coordinates (class_(*args, **kwargs))

        :param x: coordinate on the abscissa axis (0 <= x <=  size of the field)
        :param y: coordinate on the ordinate axis (0 <= x <=  size of the field)
        :param class_: class being the class of the desired cell
        :param args: positional arguments
        :param kwargs: keyword arguments

        :return: None
        """
        if x < 0:
            SpawnCellException("x cannot be negative", x, y)
        if y < 0:
            SpawnCellException("y cannot be negative", x, y)

        if x >= self.__size__[0]:
            SpawnCellException("x cannot be greater than the size of the field", x, y)
        if y >= self.__size__[1]:
            SpawnCellException("y cannot be greater than the size of the field", x, y)

        if not issubclass(class_, Cell):
            SpawnCellException("class_ is not a subclass of Cell")

        self.__need_render__[y][x] = True

        self.event.event_spawn_cell(self, x, y)  # cell spawning event

        if self.__layer_by_layer_update__:
            self.__next__cells__[y][x] = class_(*args, **kwargs)
        else:
            self.__cells__[y][x] = class_(*args, **kwargs)

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Returns the cell in the specified coordinates
        :param x: coordinate on the abscissa axis (0 <= x <=  size of the field)
        :param y: coordinate on the ordinate axis (0 <= x <=  size of the field)

        :return: the subclass Cell
        """
        if x < 0:
            GetCellException("x cannot be negative", x, y)
        if y < 0:
            GetCellException("y cannot be negative", x, y)

        if x >= self.__size__[0]:
            GetCellException("x cannot be greater than the size of the field", x, y)
        if y >= self.__size__[1]:
            GetCellException("y cannot be greater than the size of the field", x, y)

        return self.__cells__[y][x]

    def try_get_cell(self, x: int, y: int, default: type, *args, **kwargs) -> Cell:
        if x < 0:
            return default(*args, **kwargs)
        if y < 0:
            return default(*args, **kwargs)

        if x >= self.__size__[0]:
            return default(*args, **kwargs)
        if y >= self.__size__[1]:
            return default(*args, **kwargs)

        return self.__cells__[y][x]

    def get_pattern_cell(self, x: int, y: int) -> pg.Surface:
        """
        Returns the pattern cell in the specified coordinates
        :param x: coordinate on the abscissa axis (0 <= x <=  size of the field)
        :param y: coordinate on the ordinate axis (0 <= x <=  size of the field)
        :return: the pygame Surface
        """
        if x < 0:
            GetPatternCellException("x cannot be negative", x, y)
        if y < 0:
            GetPatternCellException("y cannot be negative", x, y)

        if x >= self.__size__[0]:
            GetPatternCellException("x cannot be greater than the size of the field", x, y)
        if y >= self.__size__[1]:
            GetPatternCellException("y cannot be greater than the size of the field", x, y)

        if self.__layer_by_layer_update__:
            return pg.transform.scale(
                self.__next__cells__[y][x].pattern,
                (self.__render_size_cell__, self.__render_size_cell__),
            )
        return pg.transform.scale(
            self.__cells__[y][x].pattern,
            (self.__render_size_cell__, self.__render_size_cell__),
        )

    def draw_cell(self, x: int, y: int, pattern: pg.Surface) -> None:
        """
        Draws the cell in the surface of the field
        :param x: coordinate on the abscissa axis (0 <= x <=  size of the field)
        :param y: coordinate on the ordinate axis (0 <= x <=  size of the field)
        :param pattern: pygame Surface

        :return: None
        """
        if x < 0:
            DrawCellException("x cannot be negative", x, y)
        if y < 0:
            DrawCellException("y cannot be negative", x, y)

        if x >= self.__size__[0]:
            DrawCellException("x cannot be greater than the size of the field", x, y)
        if y >= self.__size__[1]:
            DrawCellException("y cannot be greater than the size of the field", x, y)

        if pattern.get_size() != (self.__render_size_cell__, self.__render_size_cell__):
            DrawCellException("incorrect pattern size")

        self.event.event_draw_cell(self, x, y)  # cell drawing event

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
    def __render__(self):
        self.event.event_render(self, self.__need_render__)
        for y in range(len(self.__need_render__)):
            for x in range(len(self.__need_render__[y])):
                if self.__need_render__[y][x] or self.__forced_rendering_of_all_pixels__:
                    self.draw_cell(x, y, self.get_pattern_cell(x, y))
                    self.__need_render__[y][x] = False

    @time_decorator(frequency=10)
    def __update__(self):
        if self.__layer_by_layer_update__:
            self.__next__cells__ = copy.deepcopy(self.__cells__)
        self.event.event_update(self)
        for y, line_cells in enumerate(self.__cells__):
            for x, cell in enumerate(line_cells):

                self.event.event_update_cell(self, x, y)

                information = {
                    "x": x,
                    "y": y
                }

                need_update = cell.update(self, information)
                if not (need_update is None) and not (self.__need_render__[y][x]):
                    self.__need_render__[y][x] = need_update
        if self.__layer_by_layer_update__:
            self.__cells__ = self.__next__cells__


class Event:
    """object which is responsible for functions called at certain events"""

    def __init__(self) -> None:
        self.__event_update__ = {}
        self.__event_render__ = {}
        self.__event_update_cell__ = {}
        self.__event_pause_update__ = {}
        self.__event_pause_render__ = {}
        self.__event_spawn_cell__ = {}
        self.__event_draw_cell__ = {}

    def event_update(self, field):
        for event in self.__event_update__.values():
            event(field)

    def add_event_update(self, event_name, event):
        self.__event_update__[event_name] = event

    def del_event_update(self, event_name):
        del self.__event_update__[event_name]

    def event_render(self, field, need_render):
        for event in self.__event_render__.values():
            event(field, need_render)

    def add_event_render(self, event_name, event):
        self.__event_render__[event_name] = event

    def del_event_render(self, event_name):
        del self.__event_render__[event_name]

    def event_update_cell(self, field, x, y):
        for event in self.__event_update_cell__.values():
            event(field, x, y)

    def add_event_update_cell(self, event_name, event):
        self.__event_update_cell__[event_name] = event

    def del_event_update_cell(self, event_name):
        del self.__event_update_cell__[event_name]

    def event_pause_update(self, field, pause):
        for event in self.__event_pause_update__.values():
            event(field, pause)

    def add_event_pause_update(self, event_name, event):
        self.__event_pause_update__[event_name] = event

    def del_event_pause_update(self, event_name):
        del self.__event_pause_update__[event_name]

    def event_pause_render(self, field, pause):
        for event in self.__event_pause_render__.values():
            event(field, pause)

    def add_event_pause_render(self, event_name, event):
        self.__event_pause_render__[event_name] = event

    def del_event_pause_render(self, event_name):
        del self.__event_pause_render__[event_name]

    def event_spawn_cell(self, field, x, y):
        for event in self.__event_spawn_cell__.values():
            event(field, x, y)

    def add_event_spawn_cell(self, event_name, event):
        self.__event_spawn_cell__[event_name] = event

    def del_event_spawn_cell(self, event_name):
        del self.__event_spawn_cell__[event_name]

    def event_draw_cell(self, field, x, y):
        for event in self.__event_draw_cell__.values():
            event(field, x, y)

    def add_event_draw_cell(self, event_name, event):
        self.__event_draw_cell__[event_name] = event

    def del_event_draw_cell(self, event_name):
        del self.__event_draw_cell__[event_name]
