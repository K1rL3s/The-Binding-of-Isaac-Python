import math
import random
from typing import Type

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.Enemies.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.characters.parents import Body


class ShootingEnemy(BaseEnemy):
    """
    Стреляющий противник.

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param damage_from_blow: Урон получаемый от взрывов.
    :param room_graph: Графоподобный словарь клеток в комнате.
    :param main_hero: Главный персонаж (у него должен быть .rect)
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.

    :param shot_damage: Урон слезы.
    :param shot_max_distance: Максимальная дальность полёта слезы в клетках.
    :param shot_max_speed: Максимальная скорость полёта слезы в клетках.
    :param shot_delay: Задержка между выстрелами.
    :param tear_class: Класс слезы.
    :param tear_collide_groups: Группы спрайтов, с которым нужно обрабатывать столкновения слёз.

    :param groups: Группы спрайтов.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Body,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_max_speed: int | float,
                 shot_delay: int | float,
                 tear_class: Type[BaseTear],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        BaseEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero, enemy_collide_groups, *groups)

        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_max_speed = shot_max_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.tear_collide_groups = tear_collide_groups

        self.shot_ticks = random.uniform(0, self.shot_delay / 2)
        self.tears = pg.sprite.Group()

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.

        :param delta_t: Время с прошлого кадра.
        """
        self.shot_ticks += delta_t

        if self.shot_ticks >= self.shot_delay:
            self.shot()

        self.tears.update(delta_t)

    def draw_tears(self, screen: pg.Surface):
        """
        Отрисовка слёз.
        """
        self.tears.draw(screen)

    def shot(self) -> bool:
        """
        Выстрел в сторону ГГ.

        :return: Выстрелил ли.
        """
        # body
        x, y = self.main_hero.rect.center
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE or distance == 0:  # Стреляет тогда, когда уже вплотную, ну хз.
            return False

        self.shot_ticks = 0
        vx = self.shot_max_speed * dx / distance + getattr(self, 'vx', 0)  # Учёт собственной скорости
        vy = self.shot_max_speed * dy / distance + getattr(self, 'vy', 0)  # Учёт собственной скорости
        self.tear_class((self.x, self.y), self.rect.center, self.shot_damage, self.shot_max_distance, vx, vy,
                        self.tear_collide_groups, self.tears)
        return True
