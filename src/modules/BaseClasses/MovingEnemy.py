import math
from typing import Type

import pygame as pg

from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.BaseTear import BaseTear
from src.modules.BaseClasses.MoveSprite import MovableSprite
from src.utils.funcs import pixels_to_cell, cell_to_pixels
from src.utils.graph import make_path_to_cell


class MovingEnemy(BaseEnemy, MovableSprite):
    """
    Противник ходящий.

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param speed: Скорость в клетках.
    :param damage_from_blow: Урон получаемый от взрывов.
    :param move_update_delay: Задержка между перерасчётом пути до ГГ.
    :param room_graph: Графоподобный словарь клеток в комнате.
    :param shot_damage: Урон слезы.
    :param shot_max_distance: Максимальная дальность полёта слезы в клетках.
    :param shot_max_speed: Максимальная скорость полёта слезы в клетках.
    :param shot_delay: Задержка между выстрелами.
    :param tear_class: Класс слезы.
    :param main_hero: Главный персонаж (у него должен быть .rect)
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param tear_collide_groups: Группы спрайтов, с которым нужно обрабатывать столкновения слёз.
    :param groups: Группы спрайтов.
    """
    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 speed: int | float,
                 damage_from_blow: int,
                 move_update_delay: int | float,
                 room_graph: dict[tuple[int, int]],
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_max_speed: int | float,
                 shot_delay: int | float,
                 tear_class: Type[BaseTear],
                 main_hero: pg.sprite.Sprite,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 flyable: bool = False):
        movable = True
        BaseEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph,
                           shot_damage, shot_max_distance, shot_max_speed, shot_delay, tear_class,
                           main_hero, enemy_collide_groups, tear_collide_groups, *groups,
                           movable=movable, flyable=flyable)
        MovableSprite.__init__(self, xy_pos, enemy_collide_groups, *groups, acceleration=0)

        self.speed = speed
        self.move_update_delay = move_update_delay
        self.move_ticks = 0
        self.slowdown_coef: float = 1.0

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.

        :param delta_t: Время с прошлого кадра.
        """
        BaseEnemy.update(self, delta_t)
        MovableSprite.update(self, delta_t)
        self.move_ticks += delta_t

        if self.move_ticks >= self.move_update_delay:
            self.update_move_speed()

        self.move(delta_t)

    def move(self, delta_t: float):
        """
        Перемещение сущности.

        :param delta_t: Время с прошлого кадра.
        """
        MovableSprite.move(self, delta_t)

        # Проверка коллизий
        if not self.flyable:
            MovableSprite.check_collides(self)

        # Если координаты есть и если они отличаются от текущих, то обновляем скорости
        xy_cell = pixels_to_cell((self.x_center, self.y_center))
        if xy_cell and (self.x, self.y) != xy_cell:
            self.x, self.y = xy_cell
            self.update_move_speed()

    def move_back(self, xy_center: tuple[int, int]):
        """
        Обработка коллизии и изменение скоростей для обхода препятствия.

        :param xy_center: Центр спрайта, с которым было столкновение
        """
        MovableSprite.move_back(self, xy_center)
        centerx, centery = xy_center
        if (self.rect.centerx < centerx and self.vx > 0) or (self.rect.centerx > centerx and self.vx < 0):
            self.set_speed(0, self.speed if self.vy > 0 else -self.speed)
        if (self.rect.centery > centery and self.vy < 0) or (self.rect.centery < centery and self.vy > 0):
            self.set_speed(self.speed if self.vx > 0 else -self.speed, 0)

    def update_move_speed(self):
        """
        Обновление вертикальной и горизонатальной скоростей для перемещения к ГГ.
        """
        if self.flyable:  # Летающие летят напрямую ахахаха)
            dx = self.main_hero.rect.centerx - self.rect.centerx
            dy = self.main_hero.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance:
                self.set_speed(self.speed * dx / distance, self.speed * dy / distance)
            else:
                self.set_speed(0, 0)
            return

        self.move_ticks = 0
        xy_end = self.main_hero.rect.center
        xy_end = pixels_to_cell(xy_end)
        path_list = make_path_to_cell(self.room_graph, (self.x, self.y), xy_end)
        if not path_list or len(path_list) < 2:
            self.vx, self.vy = 0, 0
            return

        self.path = path_list[1:]
        next_cell = self.path[0]
        x, y = cell_to_pixels(next_cell)
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance:
            self.set_speed(self.speed * dx / distance, self.speed * dy / distance)
