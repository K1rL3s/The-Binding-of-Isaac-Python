import math
from typing import Type

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear
from src.utils.funcs import pixels_to_cell, cell_to_pixels
from src.utils.graph import make_path_to_cell


class MovingEnemy(BaseEnemy):
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
        super().__init__(xy_pos, hp, damage_from_blow, room_graph,
                         shot_damage, shot_max_distance, shot_max_speed, shot_delay, tear_class,
                         main_hero, enemy_collide_groups, tear_collide_groups, *groups,
                         movable=movable, flyable=flyable)

        self.speed = speed * CELL_SIZE
        self.move_update_delay = move_update_delay
        self.vx, self.vy = 0, 0
        self.move_ticks = 0

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.

        :param delta_t: Время с прошлого кадра.
        """
        super().update(delta_t)
        self.move_ticks += delta_t

        if self.move_ticks >= self.move_update_delay:
            self.update_move_speed()

        self.move(delta_t)

    def move(self, delta_t: float):
        """
        Перемещение сущности.

        :param delta_t: Время с прошлого кадра.
        """
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        self.x_center += self.vx * delta_t
        self.y_center += self.vy * delta_t
        self.rect.center = self.x_center, self.y_center

        # Проверка коллизий
        if not self.flyable:
            is_collided = False
            for group in self.enemy_collide_groups:
                if sprites := pg.sprite.spritecollide(self, group, False):
                    is_collided = True
                    for sprite in sprites:
                        sprite: BaseSprite
                        sprite.collide(self)
            if is_collided:
                return

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
        self.x_center, self.y_center = self.x_center_last, self.y_center_last
        self.rect.center = self.x_center, self.y_center
        centerx, centery = xy_center
        if self.rect.centerx < centerx and self.vx > 0:
            self.vy = self.speed if self.vy > 0 else -self.speed
            self.vx = 0
        if self.rect.centerx > centerx and self.vx < 0:
            self.vy = self.speed if self.vy > 0 else -self.speed
            self.vx = 0
        if self.rect.centery > centery and self.vy < 0:
            self.vx = self.speed if self.vx > 0 else -self.speed
            self.vy = 0
        if self.rect.centery < centery and self.vy > 0:
            self.vx = self.speed if self.vx > 0 else -self.speed
            self.vy = 0

    def update_move_speed(self):
        """
        Обновление вертикальной и горизонатальной скоростей для перемещения к ГГ.
        """
        if self.flyable:  # Летающие летят напрямую ахахаха)
            dx = self.main_hero.rect.centerx - self.rect.centerx
            dy = self.main_hero.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance:
                self.vx = self.speed * dx / distance
                self.vy = self.speed * dy / distance
            else:
                self.vx, self.vy = 0, 0
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
            self.vx = self.speed * dx / distance
            self.vy = self.speed * dy / distance
