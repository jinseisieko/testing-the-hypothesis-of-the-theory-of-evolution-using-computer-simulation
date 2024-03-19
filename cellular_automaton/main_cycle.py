import sys

import pygame as pg
import pyautogui

from cellular_automaton.const import SELF_SIZE, FPS


class MainCycle(object):
    def __init__(self, automatic_screen_resolution=True) -> None:
        screen_resolution: tuple[int, int] = pyautogui.size() if automatic_screen_resolution else SELF_SIZE
        self.screen: pg.Surface = pg.display.set_mode(screen_resolution)

        self.clock: pg.time.Clock = pg.time.Clock()

    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            self.screen.fill(0)

            pg.draw.rect(self.screen, (255, 255, 255), (0, 0, 10, 10))
            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    main_cycle = MainCycle()
    main_cycle.run()
