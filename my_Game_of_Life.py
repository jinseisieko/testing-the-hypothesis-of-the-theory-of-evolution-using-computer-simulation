import random

import pygame as pg

from cellular_automaton import *


class Start(Cell):
    def __init__(self):
        super().__init__()

        self.name = "Start"

    @property
    def pattern(self) -> pg.Surface:
        s = pg.Surface((100, 100))
        s.fill((255, 0, 0))
        return s

    def update(self, field, information) -> bool:
        if random.random() < 0.4:
            field.spawn_cell(information["x"], information["y"], Black)
        else:
            field.spawn_cell(information["x"], information["y"], White)

        return True

    def __repr__(self):
        return "@"


class Black(Cell):
    def __init__(self):
        super().__init__()
        self.name = "Black"

    @property
    def pattern(self) -> pg.Surface:
        s = pg.Surface((100, 100))
        s.fill((0, 0, 0))
        return s

    def update(self, field, information) -> bool:
        c = 0
        if field.try_get_cell(information["x"] + 1, information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"], information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] + 1, information["y"], default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] + 1, information["y"] - 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"], default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"], information["y"] - 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"] - 1, default=Start).name == "Black":
            c += 1

        if c != 2 and c != 3:
            field.spawn_cell(information["x"], information["y"], White)
            return True
        return False

    def __repr__(self):
        return "#"


class White(Cell):
    def __init__(self):
        super().__init__()
        self.name = "White"

    @property
    def pattern(self) -> pg.Surface:

        s = pg.Surface((100, 100))
        s.fill((255, 255, 255))
        return s

    def update(self, field, information) -> bool:
        c = 0
        if field.try_get_cell(information["x"] + 1, information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"], information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] + 1, information["y"], default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"] + 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] + 1, information["y"] - 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"], default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"], information["y"] - 1, default=Start).name == "Black":
            c += 1
        if field.try_get_cell(information["x"] - 1, information["y"] - 1, default=Start).name == "Black":
            c += 1

        if c == 3 :
            field.spawn_cell(information["x"], information["y"], Black)
            return True
        return False

    def __repr__(self):
        return " "


mc = MainCycle((50, 50),
               forced_render=False,
               render_frequency=999,
               update_frequency=20,
               layer_by_layer_update=True,
               borders=True,
               default_cell=Start,
               forced_rendering_of_all_pixels=False
               )

mc.run()
