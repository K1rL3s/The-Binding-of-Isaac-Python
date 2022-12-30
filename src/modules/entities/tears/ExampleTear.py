import pygame as pg

from src.modules.entities.tears.BaseTear import BaseTear


class ExampleTear(BaseTear):
    def __init__(self,
                 xy_pos: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.Group,
                 is_friendly: bool = False):
        super().__init__(xy_pos, damage, max_distance, vx, vy, collide_groups, *groups, is_friendly=is_friendly)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = pg.Surface((10, 10), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, 'red', (5, 5), 1)

