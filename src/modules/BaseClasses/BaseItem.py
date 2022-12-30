from typing import Any

import pygame as pg


from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.consts import CELL_SIZE, WALL_SIZE, STATS_HEIGHT


class BaseItem(BaseSprite):
    """
    Базовый класс для предметов (камень, какашка, ключ, монета, артефакт итд).

    :param sounds: Звуки, которые принадлежат объекту.
    :param textures: Текстуры, которые принадлежать объекту.
    :param groups: Все группы, которым принадлежит предмет-спрайт.
    :param acceleration: Ускорение торможения в случае movable = True
    :param colliadble: Можно ли столкнуться с объектом (непроходимый ли).
    :param destroyable: Можно ли сломать слезой.
    :param pickable: Можно ли подобрать.
    :param movable: Двигается ли после взрыва бомбы или толчка игроком.
    :param hurtable: Наносит ли урон персонажу при прикосновении.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 0,
                 collidable: bool = False,
                 destroyable: bool = False,
                 pickable: bool = False,
                 movable: bool = False,
                 hurtable: bool = False):
        super().__init__(*groups)
        self.groups = groups

        self.x, self.y = xy_pos
        self.collidable = collidable
        self.destroyable = destroyable
        self.pickable = pickable
        self.movable = movable
        self.hurtable = hurtable

        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))
        self.hp = 0
        self.vx = 0
        self.vy = 0
        self.a = acceleration

    def update(self, delta_t: float, *args, **kwargs):
        """
        Обновление положения объекта (нужно при self.movable = True)
        :param delta_t: Время с прошлого кадра.
        """
        pass
        # if self.vx or self.vy:
        #     self.rect.move_ip(ceil(self.vx * delta_t), ceil(self.vy * delta_t))
        #     if self.vx:
        #         self.vx = max((0, self.vx - self.a * delta_t))
        #     if self.vy:
        #         self.vx = max((0, self.vy - self.a * delta_t))

    def set_rect(self, width: int = None, height: int = None):
        """
        Установка объекта в центре своей клетки.
        """
        self.rect = self.image.get_rect()
        if width:
            self.rect.width = width
        if height:
            self.rect.height = height
        cell_x = self.x * CELL_SIZE + WALL_SIZE + (CELL_SIZE - self.rect.width) // 2
        cell_y = self.y * CELL_SIZE + WALL_SIZE + STATS_HEIGHT + (CELL_SIZE - self.rect.width) // 2
        if width is None:
            width = self.image.get_width()
        if height is None:
            height = self.image.get_height()
        self.rect = pg.Rect(cell_x, cell_y, width, height)
        self.mask = pg.mask.from_surface(self.image)

    def set_start_speed(self, vx: int | float, vy: int | float):
        """
        Задание начальной скорости движения.
        :param vx: Скорость по горизонтали.
        :param vy: Скорость по вертикали.
        """
        pass
        # self.vx = vx
        # self.vy = vy

    def pickup(self, *args, **kwargs):
        """
        Подбор предмета (ключ, монета, артефакт)
        """
        pass
        # self.destroy()

    def collide(self, other: Any):
        """
        Обработка столкновения с энтити.
        :param other: Объект, с которым прозошло столкновение (персонаж, слеза, взрыв бомбы).
        """
        if self.collidable:
            pass
        if self.destroyable:
            pass
        if self.pickable:
            pass
        if self.movable:
            pass
        if self.hurtable:
            pass

    def destroy(self, *args, **kwargs):
        """
        Разрушение/Удаление энтити.
        """
        pass
        # self.kill()
