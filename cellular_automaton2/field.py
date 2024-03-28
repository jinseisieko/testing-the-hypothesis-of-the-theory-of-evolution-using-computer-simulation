import copy
import time

from .cell import DefaultCell, Cell
import threading


class Settings(object):
    def __init__(self):
        self.default_cell: type = DefaultCell
        self.default_cell_args: list = []
        self.default_cell_kwargs: dict = {}

        self.update_frequency: float = 1.

        self.layer_by_layer = True
        self.optimized_rendering = True


class InformationField(object):
    def __init__(self):
        self.insufficient_update_time = [0] * 10

    def add_insufficient_update_time(self, insufficient_time):
        self.insufficient_update_time.append(insufficient_time)
        self.insufficient_update_time.pop(0)


class Field(object):
    def __init__(self, size: tuple[int, int], settings: Settings = Settings()) -> None:
        self.size: tuple[int, int] = size
        self.settings: Settings = settings
        self.information: InformationField = InformationField()

        self.cells: list = [
            [self.settings.default_cell(*self.settings.default_cell_args, **self.settings.default_cell_kwargs) for _ in
             range(size[0])] for _ in range(size[1])]

        self.need_an_update: list = [[True for _ in range(size[0])] for _ in range(size[1])]

        self.ancillary_cells: list = self.cells

        self.thread_update = threading.Thread(target=self.updating_thread)

        self.thread_update.start()

    def updating_thread(self) -> None:
        while True:
            time_start = time.time()
            self.update()
            end_time = time.time()
            time_elapsed = end_time - time_start
            print(time_elapsed)
            if time_elapsed < 1 / self.settings.update_frequency:
                time.sleep(1 / self.settings.update_frequency - time_elapsed)
            else:
                self.information.add_insufficient_update_time(time_elapsed - 1 / self.settings.update_frequency)

            print(self.information.insufficient_update_time)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def try_to_get_cell(self, x: int, y: int, default: Cell) -> Cell:
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return default
        return self.get_cell(x, y)

    def update(self) -> None:
        if self.settings.layer_by_layer:
            self.ancillary_cells = copy.deepcopy(self.cells)
        # self.event.event_update(self)
        for y, line_cells in enumerate(self.cells):
            for x, cell in enumerate(line_cells):
                # self.event.event_update_cell(self, x, y)

                information_cell = {
                    "x": x,
                    "y": y
                }

                need_an_update_cell = cell.update(self, information_cell)
                if self.settings.optimized_rendering:
                    self.need_an_update[y][x] |= need_an_update_cell
                else:
                    self.need_an_update: list = [[True for _ in range(self.size[0])] for _ in range(self.size[1])]

        if self.settings.layer_by_layer:
            self.cells = copy.deepcopy(self.ancillary_cells)
