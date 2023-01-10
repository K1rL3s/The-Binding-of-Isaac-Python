from typing import Any

import pygame as pg

from src.consts import STATS_HEIGHT
from src.modules.menus.Minimap import Minimap
from src.modules.levels.Level import Level
from src.utils.funcs import load_image


class Stats:
    """
    Класс полоски сверху.

    :param isaac: Главный герой.
    :param level: Текущий этаж.
    """
    black_line = load_image("textures/room/black_line.png")

    def __init__(self,
                 isaac: Any,
                 level: Level):
        self.isaac = isaac
        self.minimap = Minimap(level)

    def update_minimap(self):
        """
        Обновление миникарты.
        """
        self.minimap.update_minimap()

    def render(self, screen: pg.Surface):
        self.minimap.render(screen)
        screen.blit(Stats.black_line, (0, STATS_HEIGHT - Stats.black_line.get_height() // 2))
