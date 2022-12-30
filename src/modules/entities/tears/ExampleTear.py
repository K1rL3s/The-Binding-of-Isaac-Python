import random

import pygame as pg

from src.utils.funcs import crop
from src.modules.Animation import Animation
from src.modules.BaseClasses.BaseTear import BaseTear


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
        self.image = crop(BaseTear.all_tears[0][7])
        self.mask = pg.mask.from_surface(self.image)

    def destroy(self, dokill: bool = False):
        # Animation()
        super().destroy()

