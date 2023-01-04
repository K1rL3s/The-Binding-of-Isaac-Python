import math
import random

import pygame as pg

from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.MovableSprite import MovableSprite
from src.consts import CELL_SIZE
from src.utils.funcs import load_image, load_sound


class BaseTear(MovableSprite):
    all_tears: list[list[pg.Surface]] = [
        [
            load_image("textures/tears/tears.png").subsurface(x * 64, y * 64, 64, 64)
            for x in range(13)
        ]
        for y in range(2)
    ]
    all_ends: pg.surface = load_image("textures/tears/tears_pop.png")

    impacts: list[pg.mixer.Sound] = [load_sound(f"sounds/tear_impact{i}.mp3") for i in range(1, 4)]

    """
    Базовый класс слезы (Мб надо переделать).

    :param xy_pos: Позиция в комнате.
    :param xy_pixels: Координата спавна в пикселях, центр слезы.
    :param damage: Урон.
    :param distance: Дальности полёта в клетках (переделывается в pixels/sec).
    :param vx: Скорость по горизонтали в клетках (переделывается в pixels/sec).
    :param vy: Скорость по вертикали в клетках (переделывается в pixels/sec).
    :param collide_groups: Группы, с которыми надо проверять столкновение.
    :param groups: Группы спрайтов.
    :param acceleration: Ускорение торможения слезы, если надо, чтобы она тормозила.
    :param max_lifetime: Максимальное время жизни.
    :param is_friendly: Игноририует ли главного героя.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 xy_pixels: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.Group,
                 acceleration: int | float = 0,
                 max_lifetime: int | float = 0,
                 is_friendly: bool = False):
        MovableSprite.__init__(self, xy_pos, collide_groups, *groups, acceleration=acceleration, xy_pixels=xy_pixels)

        self.start_x, self.start_y = xy_pixels
        self.damage = damage
        self.max_distance = max_distance
        self.vx, self.vy = vx, vy
        self.collide_groups = collide_groups
        self.groups = groups
        self.is_friendly = is_friendly
        self.max_lifetime = max_lifetime
        self.lifetime_ticks = 0

        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))

    def update(self, delta_t: float):
        """
        Обновление положения слезы.

        :param delta_t: Время с прошлого кадра.
        """
        self.lifetime_ticks += delta_t

        MovableSprite.move(self, delta_t)
        self.check_collides()

        if math.hypot(self.start_x - self.rect.x, self.start_y - self.rect.y) > self.max_distance * CELL_SIZE:
            self.destroy()
        elif self.max_lifetime and self.lifetime_ticks >= self.max_lifetime:
            self.destroy()

    def check_collides(self):
        for collide_group in self.collide_groups:
            if pg.sprite.spritecollideany(self, collide_group):
                for collide in pg.sprite.spritecollide(self, collide_group, False):
                    collide: BaseSprite
                    collide.hurt(self.damage)
                    collide.collide(self)

    def set_rect(self, width: int = None, height: int = None):
        """
        Установка rect и mask слезы.
        """
        width, height = self.image.get_width(), self.image.get_height()
        self.rect = pg.Rect(self.start_x - width // 2, self.start_y - height // 2, width, height)
        self.mask = pg.mask.from_surface(self.image)

    def destroy(self):
        """
        Смерть слезы...
        """
        random.choice(BaseTear.impacts).play()
        self.kill()
