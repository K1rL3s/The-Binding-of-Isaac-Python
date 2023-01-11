import pygame as pg

from src.modules.levels.Level import Level
from src.modules.levels.Room import Room
from src.modules.menus.Stats import Stats
from src.consts import FloorsTypes, Moves, GAME_HEIGHT, GAME_WIDTH, STATS_HEIGHT
from src.modules.characters.parents import Player
#from src.modules.BaseClasses.dddddEnemies.BaseEnemy import BaseEnemy


# Заглушка (переделать!)
class Game:
    def __init__(self):
        # ЗАТЫЧКА ГГ BaseEnemy((0, 0), 10, 10, dict(), None, None)

        self.main_hero = Player((300, 500), 100, 10, 10, 4, 5, 2)

        # ЗАТЫЧКА ГГ

        self.screen = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.levels = [Level(floor_type, self.main_hero) for floor_type in FloorsTypes]
        self.current_level = self.levels[0]
        self.current_level.update_main_hero_collide_groups()
        self.stats = Stats(None, self.current_level)

    def get_current_level_rooms(self) -> list[list[Room | None]]:
        return self.current_level.get_rooms()

    def move_to_next_level(self):
        self.current_level = self.levels[(self.levels.index(self.current_level) + 1) % len(self.levels)]
        self.current_level.update_main_hero_collide_groups()
        self.stats = Stats(None, self.current_level)

    def move_to_next_room(self, direction: Moves):
        self.current_level.move_to_next_room(direction)
        self.current_level.update_main_hero_collide_groups()
        self.stats.update_minimap()

    def move_main_hero(self, xy_pos: tuple[int, int]):
        x, y = xy_pos
        y -= STATS_HEIGHT
        self.main_hero.body.rect = pg.Rect(x - self.main_hero.body.rect.width // 2,
                                           y - self.main_hero.body.rect.height // 2,
                                           self.main_hero.body.rect.width,
                                           self.main_hero.body.rect.height)

    def update(self, delta_t: float):
        self.current_level.update(delta_t)
        self.main_hero.update(delta_t)

    def render(self, screen: pg.Surface):
        self.stats.render(screen)
        self.current_level.render(self.screen)
        screen.blit(self.screen, (0, STATS_HEIGHT))
