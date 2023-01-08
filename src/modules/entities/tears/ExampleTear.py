import pygame as pg

from src.utils.funcs import crop
from src.modules.animations.Animation import Animation
from src.modules.BaseClasses.Based.BaseTear import BaseTear


class ExampleTear(BaseTear):
    def __init__(self,
                 xy_pos: tuple[int, int],
                 xy_pixels: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.Group):
        is_friendly = False
        BaseTear.__init__(self, xy_pos, xy_pixels, damage, max_distance, vx, vy, collide_groups, *groups,
                          is_friendly=is_friendly)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = crop(BaseTear.all_tears[0][1])
        self.mask = pg.mask.from_surface(self.image)

    def destroy(self, dokill: bool = False):
        # Animation()  # Сделать анимацию
        BaseTear.destroy(self)

