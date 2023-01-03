import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.BaseSprite import BaseSprite

from src.utils.funcs import cell_to_pixels


class MovableItem(BaseItem):
    """
    Передвигаемый предмет.

    :param xy_pos: Позиция в комнате.
    :param acceleration: Ускорение торможения в клетках/секунду.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    :param pickable: Можно ли подобрать.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 acceleration: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None,
                 pickable: bool = False):
        super().__init__(xy_pos, *groups, pickable=pickable, movable=True, collidable=False)

        self.a = acceleration
        self.collide_groups = collide_groups

        if xy_pixels:
            self.x_center, self.y_center = xy_pixels
        else:
            self.x_center, self.y_center = cell_to_pixels(xy_pos)
        self.x_center_last, self.y_center_last = self.x_center, self.y_center

    def set_rect(self, width: int = None, height: int = None):
        """
        Установка объекта в центре своей клетки.
        """
        super().set_rect()
        if (self.x_center, self.y_center) != cell_to_pixels((self.x, self.y)):
            self.rect.center = (self.x_center, self.y_center)

    def set_speed(self, vx: int | float, vy: int | float):
        """
        Задание скорости движения.

        :param vx: Скорость по горизонтали в клетках/секунду.
        :param vy: Скорость по вертикали в клетках/секунду.
        """
        self.vx = vx
        self.vy = vy

    def move(self, delta_t: float):
        """
        Перемещение объекта и изменение его скоростей.

        :param delta_t: Время с прошлого кадра.
        """
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        if self.vx:
            if self.vx < 0:
                self.vx = min((0, self.vx + self.a * delta_t))
            else:
                self.vx = max((0, self.vx - self.a * delta_t))
        if self.vy:
            if self.vy < 0:
                self.vy = min((0, self.vy + self.a * delta_t))
            else:
                self.vy = max((0, self.vy - self.a * delta_t))
        self.x_center += self.vx * CELL_SIZE * delta_t
        self.y_center += self.vy * CELL_SIZE * delta_t
        self.rect.center = self.x_center, self.y_center

        for group in self.collide_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    sprite: BaseSprite
                    sprite.collide(self)

    def move_back(self, xy_center: tuple[int, int]):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param xy_center: Центр спрайта, с которым было столкновение
        """
        self.x_center, self.y_center = self.x_center_last, self.y_center_last
        self.rect.center = self.x_center, self.y_center
        centerx, centery = xy_center
        if self.rect.centerx < centerx and self.vx > 0:
            self.vx = 0
        if self.rect.centerx > centerx and self.vx < 0:
            self.vx = 0
        if self.rect.centery > centery and self.vy < 0:
            self.vy = 0
        if self.rect.centery < centery and self.vy > 0:
            self.vy = 0

    def collide(self, other: BaseSprite):
        """
        Не факт, что работает корректно :)
        Пока что супер примитивно, ага
        """
        super().collide(other)
        vx = 1 if self.rect.centerx - other.rect.centerx > 0 else -1
        vy = 1 if self.rect.centery - other.rect.centery > 0 else -1
        self.set_speed(self.vx + vx, self.vy + vy)
