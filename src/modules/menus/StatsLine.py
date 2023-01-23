from typing import Any

import pygame as pg

from src.consts import STATS_HEIGHT
from src.modules.menus.Minimap import Minimap
from src.modules.menus.HeroStats import HeroStats
from src.modules.levels.Level import Level
from src.utils.funcs import load_image


class Stats:
    """
    Класс полоски сверху.

    :param main_hero: Главный герой.
    :param level: Текущий этаж.
    """
    black_line = load_image("textures/room/black_line.png")

    def __init__(self,
                 main_hero: Any,
                 level: Level):
        self.main_hero = main_hero
        self.minimap = Minimap(level)
        self.hero_stats = HeroStats(main_hero)

    def update_minimap(self):
        """
        Обновление миникарты.
        """
        self.minimap.update_minimap()

    def update_hero_stats(self):
        """
        Обновление статистики персонажа.
        """
        self.hero_stats.update()

    def render(self, screen: pg.Surface):
        self.minimap.render(screen)
        self.hero_stats.render(screen)
        screen.blit(Stats.black_line, (0, STATS_HEIGHT - Stats.black_line.get_height() // 2))
