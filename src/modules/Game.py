import pygame as pg

from src.modules.levels.Level import Level
from src.modules.levels.Room import Room
from src.modules.menus.Stats import Stats
from src.consts import FloorsTypes, Moves

from src.modules.BaseClasses.BaseEnemy import BaseEnemy


# Заглушка (переделать!)
class Game:
    def __init__(self):
        # ЗАТЫЧКА ГГ
        self.main_hero = BaseEnemy((0, 0), 10, 10, 1, dict(), 10, 10, 10, 10, None, None, None, None)
        self.main_hero.image = pg.Surface((50, 50))
        pg.draw.rect(self.main_hero.image, 'black', (0, 0, 50, 50))
        self.main_hero.rect = pg.Rect(0, 0, 50, 50)
        # ЗАТЫЧКА ГГ

        self.levels = [Level(floor_type, self.main_hero) for floor_type in FloorsTypes]
        self.current_level = self.levels[0]
        self.stats = Stats(None, self.current_level)

    def get_current_level_rooms(self) -> list[list[Room | None]]:
        return self.current_level.get_rooms()

    def next_level(self):
        self.current_level = self.levels[(self.levels.index(self.current_level) + 1) % len(self.levels)]
        self.stats = Stats(None, self.current_level)

    def move_to_next_room(self, direction: Moves | tuple[int, int]):
        self.current_level.move_to_next_room(direction)
        self.stats.update_minimap()

    def move_main_hero(self, xy_pos: tuple[int, int]):
        x, y = xy_pos
        self.main_hero.rect = pg.Rect(x - self.main_hero.rect.width // 2, y - self.main_hero.rect.height // 2,
                                      self.main_hero.rect.width, self.main_hero.rect.height)

    def update(self, delta_t: float):
        self.current_level.update(delta_t)

    def render(self, screen: pg.Surface):
        self.current_level.render(screen)
        self.stats.render(screen)
