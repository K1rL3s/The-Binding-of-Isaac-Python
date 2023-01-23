import pygame as pg

from src.modules.BaseClasses.Based.BaseGame import BaseGame
from src.modules.handlers.MainHeroActionsHandler import MainHeroActionsHandler
from src.modules.levels.Level import Level
from src.modules.levels.Room import Room
from src.modules.menus.Stats import Stats
from src.utils.funcs import cell_to_pixels
from src.modules.characters.parents import Player
from src.consts import (FloorsTypes, Moves, GAME_HEIGHT, GAME_WIDTH, STATS_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT, CELL_SIZE,
                        MOVE_TO_NEXT_ROOM, MOVE_TO_NEXT_LEVEL, PICKUP_LOOT, PICKUP_ART, BUY_ITEM, USE_BOMB)
from src.modules.BaseClasses.Enemies.BaseEnemy import BaseEnemy


# Заглушка (переделать!)
class Game(BaseGame):
    def __init__(self, main_screen: pg.Surface, fps: int = 60):

        self.main_hero = Player('isaac', 100, 4, 10, 2, 5, 5, 0.5)

        BaseGame.__init__(self, main_screen, fps)
        self.level_screen = pg.Surface((GAME_WIDTH, GAME_HEIGHT))

        self.levels = [Level(floor_type, self.main_hero) for floor_type in FloorsTypes]
        self.current_level = self.levels[0]
        self.current_level.update_main_hero_collide_groups()
        self.stats = Stats(None, self.current_level)

        self.main_hero_handler = MainHeroActionsHandler(self.main_hero)

    def setup(self):
        self.register_event(pg.KEYDOWN, self.main_hero_handler.keyboard_handler)
        self.register_event(pg.KEYUP, self.main_hero_handler.keyboard_handler)
        self.register_event(MOVE_TO_NEXT_LEVEL, self.move_to_next_level)
        self.register_event(MOVE_TO_NEXT_ROOM, self.move_to_next_room)
        self.register_event(PICKUP_LOOT, self.main_hero_handler.loot_pickup_handler)
        self.register_event(PICKUP_ART, self.main_hero_handler.artifact_pickup_handler)
        self.register_event(BUY_ITEM, self.main_hero_handler.buy_handler)
        self.register_event(USE_BOMB, self.current_level.current_room.set_bomb)

    def get_current_level_rooms(self) -> list[list[Room | None]]:
        """
        Получить все комнаты текущего этажа.

        :return: Двумерный массив комнат.
        """
        return self.current_level.get_rooms()

    def move_to_next_level(self, *args):
        """
        Переход на следующий этаж.
        """
        self.current_level = self.levels[(self.levels.index(self.current_level) + 1) % len(self.levels)]
        self.current_level.update_main_hero_collide_groups()
        self.move_main_hero((ROOM_WIDTH // 2 * CELL_SIZE, ROOM_HEIGHT // 2 * CELL_SIZE))
        self.stats = Stats(None, self.current_level)

    def move_to_next_room(self, event: pg.event.Event):
        """
        Переход в другую комнату.

        :param event: Ивент, который имеет direction (вызывается дверью).
        """
        self.current_level.move_to_next_room(event.direction)
        self.current_level.update_main_hero_collide_groups()
        self.stats.update_minimap()

    def move_main_hero(self, xy_pos: tuple[int, int]):
        self.main_hero.move_to_cell(xy_pos)
        """
        Передвинуть главного героя по координатам.

        :param xy_pos: Координаты центра.
        """

    def update(self, delta_t: float):
        self.current_level.update(delta_t)
        self.main_hero.update(delta_t)

    def draw(self, screen: pg.Surface):
        self.stats.render(self.main_screen)
        self.current_level.render(self.level_screen)
        screen.blit(self.level_screen, (0, STATS_HEIGHT))


