import pygame as pg

# from src.modules.Game import Game
from src.consts import MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT


# Переделать! циклический импорт!!! (сделать класс миникарты отдельно?)
class Stats:
    def __init__(self,
                 game):  # Game):
        self.game = game
        self.rooms = game.get_current_level_rooms()
        self.level_map = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))

    def update_level_map(self):
        """
        Обновление миникарты
        """
        self.rooms = self.game.get_current_level_rooms()
        surface = pg.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
        pg.draw.rect(surface, 'red', surface.get_rect())
        for y, row in enumerate(self.rooms):
            for x, col in enumerate(row):
                if self.rooms[y][x]:
                    if self.rooms[y][x].visited:
                        color = pg.Color((255, 255, 255))
                    elif self.rooms[y][x].spotted:
                        color = pg.Color((100, 100, 100))
                    else:
                        color = pg.Color((0, 0, 0))
                    cell = pg.Surface((MINIMAP_CELL_WIDTH - 1, MINIMAP_CELL_HEIGHT - 1))
                    pg.draw.rect(cell, color, cell.get_rect())
                    surface.blit(cell, (x * MINIMAP_CELL_WIDTH, y * MINIMAP_CELL_HEIGHT))
        self.level_map = surface

    def render(self, screen: pg.Surface):
        screen.blit(self.level_map, (10, 10))


