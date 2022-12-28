import pygame as pg

from src.modules.levels.Level import Level
from src.modules.levels.Room import Room
from src.modules.menus.Stats import Stats
from src.consts import FloorsTypes, Moves


# Заглушка (переделать!)
class Game:
    def __init__(self):
        self.levels = [Level(floor_type) for floor_type in FloorsTypes]
        self.current_level = self.levels[0]
        self.stats = Stats(self)
        self.stats.update_level_map()

    def get_current_level_rooms(self) -> list[list[Room | None]]:
        return self.current_level.get_rooms()

    def next_level(self):
        self.current_level = self.levels[(self.levels.index(self.current_level) + 1) % len(self.levels)]
        self.stats.update_level_map()

    def move_to_next_room(self, direction: Moves | tuple[int, int]):
        self.current_level.move_to_next_room(direction)
        self.stats.update_level_map()

    def update(self, delta_t: float):
        self.current_level.update(delta_t)

    def render(self, screen: pg.Surface):
        self.current_level.render(screen)
        self.stats.render(screen)

