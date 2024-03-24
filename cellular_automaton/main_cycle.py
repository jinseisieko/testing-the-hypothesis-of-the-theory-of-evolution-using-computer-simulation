import sys

import pygame as pg
import pyautogui

from .field import Field
from .const import SELF_SIZE, FPS


class MainCycle(object):
    def __init__(
            self,
            size: tuple[int, int],
            forced_render: bool = False,
            update_frequency: int = 30,
            render_frequency: int = FPS,
            automatic_screen_resolution=True,
            borders=True,
    ) -> None:
        self.forced_render = forced_render
        self.position: tuple[int, int] = (0, 0)
        self.directions = [False, False, False, False]
        self.speed = 10

        pg.init()

        screen_resolution: tuple[int, int] = (
            pyautogui.size() if automatic_screen_resolution else SELF_SIZE
        )
        self.screen: pg.Surface = pg.display.set_mode(screen_resolution)
        self.clock: pg.time.Clock = pg.time.Clock()

        self.field: Field = Field(
            size,
            borders=borders,
            update_frequency=update_frequency,
            render_frequency=render_frequency,
        )

    def render(self) -> None:
        if self.forced_render:
            self.field.__render__()

    def run(self) -> None:
        self.field.start_thread_update()

        if not self.forced_render:
            self.field.start_thread_render()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.directions[0] = True
                    if event.key == pg.K_DOWN:
                        self.directions[1] = True
                    if event.key == pg.K_RIGHT:
                        self.directions[2] = True
                    if event.key == pg.K_LEFT:
                        self.directions[3] = True

                    if event.key == pg.K_p:
                        self.field.__pause_update__ = not self.field.__pause_update__

                    if event.key == pg.K_f:
                        self.field.__count_frames_update__ += 1

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.directions[0] = False
                    if event.key == pg.K_DOWN:
                        self.directions[1] = False
                    if event.key == pg.K_RIGHT:
                        self.directions[2] = False
                    if event.key == pg.K_LEFT:
                        self.directions[3] = False
            if self.directions[0]:
                self.position = (self.position[0], self.position[1] + self.speed)
            if self.directions[1]:
                self.position = (self.position[0], self.position[1] - self.speed)
            if self.directions[2]:
                self.position = (self.position[0] - self.speed, self.position[1])
            if self.directions[3]:
                self.position = (self.position[0] + self.speed, self.position[1])

            self.screen.fill(0)

            self.render()
            self.screen.blit(self.field.__surface__, self.position)
            self.screen.blit(
                pg.font.Font(None, 48).render(
                    f"{round(self.clock.get_fps())}", True, (255, 255, 255)
                ),
                (0, 0),
            )

            pg.display.flip()
            self.clock.tick(FPS)
