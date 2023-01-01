import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.BaseItem import BaseItem

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
        super().__init__(xy_pos, *groups, pickable=pickable, movable=True, collidable=True)

        self.a = acceleration * CELL_SIZE
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

    def set_start_speed(self, vx: int | float, vy: int | float):
        """
        Задание начальной скорости движения.
        :param vx: Скорость по горизонтали в клетках/секунду.
        :param vy: Скорость по вертикали в клетках/секунду.
        """
        self.vx = vx * CELL_SIZE
        self.vy = vy * CELL_SIZE

    def move(self, delta_t: float):
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        if self.vx:
            if self.vx < 0:
                self.vx = min(0, self.vx + self.a * delta_t)
            else:
                self.vx = max(0, self.vx - self.a * delta_t)
        if self.vy:
            if self.vy < 0:
                self.vy = min(0, self.vy + self.a * delta_t)
            else:
                self.vy = max(0, self.vy - self.a * delta_t)
        self.x_center += self.vx * delta_t
        self.y_center += self.vy * delta_t
        self.rect.center = self.x_center, self.y_center

        for group in self.collide_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    self.move_back(sprite.rect.center)

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
