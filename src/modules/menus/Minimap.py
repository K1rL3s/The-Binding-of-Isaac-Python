import pygame as pg


from src.modules.levels import Level
from src.consts import MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT


class Minimap:
    """
    Класс миникарты.

    :param level: Текущий этаж.
    """
    def __init__(self,
                 level: Level):
        self.level = level
        self.minimap = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
        self.update_minimap()

    def update_minimap(self):
        """
        Обновление миникарты.
        """
        rooms = self.level.get_rooms()
        surface = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT), pg.SRCALPHA, 32)
        for y, row in enumerate(rooms):
            for x, col in enumerate(row):
                if rooms[y][x]:
                    cell = rooms[y][x].get_minimap_cell()
                    surface.blit(cell, (x * MINIMAP_CELL_WIDTH, y * MINIMAP_CELL_HEIGHT))
        self.minimap = surface

    def render(self, screen: pg.Surface):
        screen.blit(self.minimap, (MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT // 2))
