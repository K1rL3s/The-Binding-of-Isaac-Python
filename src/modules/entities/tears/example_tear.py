import pygame as pg

from src.modules.animations.animation import Animation
from src.modules.base_classes.based.base_tear import BaseTear
from src.utils.funcs import crop


class ExampleTear(BaseTear):
    pop_animation = BaseTear.all_ends.subsurface(
        0,
        BaseTear.height,
        BaseTear.width,
        BaseTear.height,
    )
    fps_animation = 30

    def __init__(
        self,
        xy_pos: tuple[int, int],
        xy_pixels: tuple[int, int],
        damage: int,
        max_distance: int | float,
        vx: int | float,
        vy: int | float,
        collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        *groups: pg.sprite.Group,
    ):
        is_friendly = False
        BaseTear.__init__(
            self,
            xy_pos,
            xy_pixels,
            damage,
            max_distance,
            vx,
            vy,
            collide_groups,
            *groups,
            is_friendly=is_friendly,
        )

        self.animation = Animation(
            ExampleTear.pop_animation,
            16,
            1,
            self.fps_animation,
            True,
        )
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = crop(BaseTear.all_tears[1][5])
