import random

import arcade
from cellular_automaton2.field import Field

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Cellular Automaton"


class Window(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_update_rate(1 / 120)

        self.field = Field((200, 200))
        self.size_cell = 10

    def on_update(self, dt):
        ...

    def on_draw(self):
        self.clear()
        for x, line in enumerate(self.field.need_an_update):
            for y, need_update_cell in enumerate(line):
                if True:
                    arcade.draw_rectangle_filled(x * 5 + 10, y * 5 + 10, 4, 4,
                                                 (random.randint(0, 255), 255, 255))
                self.field.need_an_update[y][x] = False


if __name__ == '__main__':
    Window()
    arcade.run()
