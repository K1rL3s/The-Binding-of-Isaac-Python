import pygame as pg
from math import ceil

from src.consts import CELL_SIZE, WALL_SIZE, STATS_HEIGHT


class BaseEntity(pg.sprite.Sprite):
    """
    Базовый класс для энитити (камень, какашка, ключ, монета, артефакт итд).

    :param sounds: Звуки, которые принадлежат объекту.
    :param textures: Текстуры, которые принадлежать объекту.
    :param groups: Все группы, которым принадлежит энтити-спрайт.
    :param acceleration: Ускорение торможения в случае movable = True
    :param colliadble: Можно ли столкнуться с объектом (непроходимый ли).
    :param destroyable: Можно ли сломать слезой.
    :param pickable: Можно ли подобрать.
    :param movable: Двигается ли после взрыва бомбы или толчка игроком.
    """

    def __init__(self, xy_pos: tuple[int, int],
                 sounds: list[pg.mixer.Sound] | dict[str,
                                                     pg.mixer.Sound |
                                                     dict[str, pg.mixer.Sound | list[pg.mixer.Sound]] |
                                                     list[pg.mixer.Sound]],
                 textures: dict[str,
                                pg.Surface |
                                dict[str, pg.Surface | list[pg.Surface]] |
                                list[pg.Surface]],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 0,
                 collidable: bool = False,
                 destroyable: bool = False,
                 pickable: bool = False,
                 movable: bool = False):
        super().__init__(*groups)
        self.groups = groups

        self.x, self.y = xy_pos
        self.sounds = sounds
        self.textures = textures
        self.collidable = collidable
        self.destroyable = destroyable
        self.pickable = pickable
        self.movable = movable

        self.image: pg.Surface
        self.rect: pg.Rect
        self.hp = 0
        self.vx = 0
        self.vy = 0
        self.a = acceleration

    def update(self, delta_t: float, *args, **kwargs):
        """
        Обновление энтити (нужно при self.movable = True)
        :param delta_t: Время с прошлого кадра.
        """
        if self.vx or self.vy:
            self.rect.move_ip(ceil(self.vx * delta_t), ceil(self.vy * delta_t))
            if self.vx:
                self.vx = max((0, self.vx - self.a * delta_t))
            if self.vy:
                self.vx = max((0, self.vy - self.a * delta_t))

    def set_image(self, *args, **kwargs):
        """
        Установка текстуры на объект.
        """
        raise NotImplementedError()

    def set_rect(self):
        """
        Установка объекта в центре своей клетки.
        """
        self.rect = self.image.get_rect()
        cell_x = self.x * CELL_SIZE + WALL_SIZE + (CELL_SIZE - self.rect.width) // 2
        cell_y = self.y * CELL_SIZE + WALL_SIZE + STATS_HEIGHT + (CELL_SIZE - self.rect.width) // 2
        self.rect = pg.Rect(cell_x, cell_y, self.image.get_width(), self.image.get_height())

    def set_start_speed(self, vx: int | float, vy: int | float):
        """
        Задание начальной скорости после начала движения.
        :param vx: Скорость по горизонтали.
        :param vy: Скорость по вертикали.
        """
        self.vx = vx
        self.vy = vy

    def pickup(self, *args, **kwargs):
        """
        Подбор предмета (ключ, монета, артефакт)
        """
        raise NotImplementedError()
        # self.destroy()

    def hurt(self, damage: int):
        """
        Нанесение урона энтити (какашке).
        :param damage: Сколько урона нанеслось.
        """
        raise NotImplementedError()
        # self.hp = max(0, self.hp - damage)
        # if self.hp == 0:
        #     self.destroy()

    def destroy(self, *args, **kwargs):
        """
        Разрушение/Удаление энтити.
        """
        raise NotImplementedError()
        # self.kill()
