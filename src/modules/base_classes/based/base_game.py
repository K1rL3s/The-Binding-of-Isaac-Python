import collections
from collections.abc import Callable

import pygame as pg


class BaseGame:
    def __init__(self, main_screen: pg.Surface, fps: int = 0):
        self.fps = fps

        self.running = False
        self.background = pg.Color(0, 0, 0)

        self.main_screen = main_screen

        self.event_handlers: dict[int, list[Callable[[pg.event.Event], None]]] = (
            collections.defaultdict(list)
        )

    def setup(self):
        pass

    def register_event(self, event_type: int, action: Callable[[pg.event.Event], None]):
        self.event_handlers[event_type].append(action)

    def start(self):
        timer = pg.time.Clock()

        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if callbacks := self.event_handlers[event.type]:
                    for callback in callbacks:
                        callback(event)
            delta_t = timer.tick(self.fps) / 1000
            self.main_screen.fill(self.background)
            self.update(delta_t)
            self.draw(self.main_screen)
            pg.display.flip()

    def update(self, delta_t: float):
        pass

    def draw(self, screen: pg.Surface):
        pass
