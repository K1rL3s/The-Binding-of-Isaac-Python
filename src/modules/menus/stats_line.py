import pygame as pg

from src.consts import STATS_HEIGHT
from src.modules.characters.main_hero import Player
from src.modules.levels.level import Level
from src.modules.menus.hero_stats import HeroStats
from src.modules.menus.minimap import Minimap
from src.utils.funcs import load_image


class Stats:
    """
    Класс полоски сверху.

    :param main_hero: Главный герой.
    :param level: Текущий этаж.
    """

    black_line = load_image("textures/room/black_line.png")

    def __init__(self, main_hero: Player, level: Level):
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
        screen.blit(
            Stats.black_line,
            (0, STATS_HEIGHT - Stats.black_line.get_height() // 2),
        )
