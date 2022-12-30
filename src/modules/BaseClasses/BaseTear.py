import math

import pygame as pg

from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.consts import CELL_SIZE


class BaseTear(BaseSprite):
    """
    Базовый класс слезы (Мб надо переделать)

    :param xy_pos: Координата спавна в пикселях, центр слезы.
    :param damage: Урон.
    :param distance: Дальности полёта в клетках (переделывается в pixels/sec).
    :param vx: Скорость по горизонтали в клетках (переделывается в pixels/sec).
    :param vy: Скорость по вертикали в клетках (переделывается в pixels/sec).
    :param collide_groups: Группы, с которыми надо проверять столкновение.
    :param groups: Группы спрайтов
    :param is_friendly: Игноририует ли главного героя.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.Group,
                 is_friendly: bool = False):
        super().__init__(*groups)

        self.cur_x, self.cur_y = self.start_x, self.start_y = xy_pos
        self.damage = damage
        self.max_distance = max_distance * CELL_SIZE
        self.vx = vx * CELL_SIZE
        self.vy = vy * CELL_SIZE
        self.vx_round = math.ceil if vx > 0 else math.floor
        self.vy_round = math.ceil if vy > 0 else math.floor
        self.collide_groups = collide_groups
        self.groups = groups
        self.is_friendly = is_friendly

        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))

    def update(self, delta_t: float):
        """
        Обновление положения слезы.
        :param delta_t: Время с прошлого кадра.
        """
        is_collided = False
        self.cur_x += self.vx * delta_t
        self.cur_y += self.vy * delta_t
        self.rect = pg.Rect(self.cur_x, self.cur_y, self.rect.width, self.rect.height)
        for collide_group in self.collide_groups:
            if pg.sprite.spritecollideany(self, collide_group):
                is_collided = True
                collides = pg.sprite.spritecollide(self, collide_group, False)
                for collide in collides:
                    collide: BaseItem  # BaseEnemy
                    collide.hurt(self.damage)  # Все спрайты из этих групп обязаны иметь метод hurt
        if is_collided:
            self.end_animation("hit")

        if math.hypot(self.start_x - self.rect.x, self.start_y - self.rect.y) > self.max_distance:
            self.end_animation("miss")

    def set_rect(self):
        """
        Установка rect и mask слезы.
        """
        width, height = self.image.get_width(), self.image.get_height()
        self.rect = pg.Rect(self.start_x - width // 2, self.start_y - height // 2, width, height)
        self.mask = pg.mask.from_surface(self.image)

    def end_animation(self, animation_type: str):
        ...
        self.kill()
