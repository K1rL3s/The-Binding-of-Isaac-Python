from typing import Type
import math

import pygame as pg

from src.consts import CELL_SIZE, WALL_SIZE, STATS_HEIGHT
from src.modules.entities.tears.BaseTear import BaseTear


class BaseEnemy(pg.sprite.Sprite):
    """
    Базовый класс противника (Ростик, измени под свой класс BaseTear).

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param speed: Скорость в клетках.
    :param shot_damage: Урон слезы.
    :param shot_max_distance: Максимальная дальность полёта слезы в клетках.
    :param shot_max_speed: Максимальная скорость полёта слезы в клетках.
    :param shot_delay: Задержка между выстрелами.
    :param tear_class: Класс слезы.
    :param main_hero: Главный персонаж (у него должен быть .rect)
    :param tear_collide_groups: Группы спрайтов, с которым нужно обрабатывать столкновения слёз.
    :param groups: Группы спрайтов.
    :param movable: Передвигается ли.
    :param flyable: Летает ли.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 speed: int | float,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_max_speed: int | float,
                 shot_delay: int | float,
                 tear_class: Type[BaseTear],
                 main_hero: pg.sprite.Sprite,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 movable: bool = False,
                 flyable: bool = False):
        super().__init__(*groups)
        self.groups = groups

        self.x, self.y = xy_pos
        self.hp = hp
        self.speed = speed * CELL_SIZE
        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_max_speed = shot_max_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.main_hero = main_hero
        self.tear_collide_groups = collide_groups
        self.movable = movable
        self.flyable = flyable

        self.ticks = 0
        self.tears = pg.sprite.Group()
        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.
        :param delta_t: Время с прошлого кадра.
        """
        self.ticks += delta_t
        if self.ticks >= self.shot_delay:
            self.shot(self.main_hero.rect.center)
            self.ticks = 0
        self.tears.update(delta_t)

    def draw_tears(self, screen: pg.Surface):
        self.tears.draw(screen)

    def set_image(self, *args, **kwargs):
        """
        Установка текстуры.
        """
        pass

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

    def shot(self, xy_pos: tuple[int, int]):
        """
        Выстрел в сторону точку xy_pos (в пикселях)
        :param xy_pos: Позиция куда стрелять
        """
        x, y = xy_pos
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE:
            return
        vx = self.shot_max_speed * dx / distance
        vy = self.shot_max_speed * dy / distance
        self.tear_class(self.rect.center, self.shot_damage, self.shot_max_distance, vx, vy,
                        self.tear_collide_groups, self.tears)

    def blow(self):
        """
        Взрыв противника.
        """
        pass

    def hurt(self, damage: int):
        """
        Нанесение урона противнику.
        :param damage: Сколько урона нанеслось.
        """
        pass
        # self.hp = max(0, self.hp - damage)
        # if self.hp == 0:
        #     self.destroy()

    def death(self):
        """
        Смерть врага.
        """
        self.kill()
