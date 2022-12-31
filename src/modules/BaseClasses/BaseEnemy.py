from typing import Type
import math

import pygame as pg

from src.utils.funcs import pixels_to_cell, cell_to_pixels
from src.utils.graph import make_path_to_cell
from src.consts import CELL_SIZE, WALL_SIZE, STATS_HEIGHT
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear


class BaseEnemy(BaseSprite):
    """
    Базовый класс противника (Ростик, измени под свой класс BaseTear).

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param speed: Скорость в клетках.
    :param move_delay: Задержка между перерасчётом пути до ГГ.
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
    :param movable: Передвигается ли.
    :param flyable: Летает ли.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 speed: int | float,
                 move_delay: int | float,
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
                 movable: bool = False,
                 flyable: bool = False):
        super().__init__(*groups)
        self.groups = groups

        self.x, self.y = xy_pos
        self.hp = hp
        self.speed = speed * CELL_SIZE
        self.move_delay = move_delay
        self.room_graph = room_graph
        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_max_speed = shot_max_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.tear_collide_groups = tear_collide_groups
        self.movable = movable
        self.flyable = flyable

        self.vx, self.vy = 0, 0
        self.x_center, self.y_center = cell_to_pixels(xy_pos)
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        self.path: list[tuple[int, int]] = []
        self.shot_ticks = 0
        self.move_ticks = 0
        self.tears = pg.sprite.Group()
        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.
        :param delta_t: Время с прошлого кадра.
        """
        self.shot_ticks += delta_t
        self.move_ticks += delta_t

        if self.shot_ticks >= self.shot_delay:
            self.shot()

        if self.move_ticks >= self.move_delay:
            self.update_move_speed()

        self.move(delta_t)
        self.tears.update(delta_t)

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

    def draw_tears(self, screen: pg.Surface):
        """
        Отрисовка слёз.
        """
        self.tears.draw(screen)

    def shot(self):
        """
        Выстрел в сторону ГГ.
        """
        self.shot_ticks = 0
        if not (self.vx or self.vy):
            return
        x, y = self.main_hero.rect.center
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE:
            return
        vx = self.shot_max_speed * dx / distance
        vy = self.shot_max_speed * dy / distance
        self.tear_class(self.rect.center, self.shot_damage, self.shot_max_distance, vx, vy,
                        self.tear_collide_groups, self.tears)

    def move(self, delta_t: float):
        """
        Перемещение сущности.
        :param delta_t: Время с прошлого кадра.
        """
        # Обновление положения
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        self.x_center = self.x_center + self.vx * delta_t
        self.y_center = self.y_center + self.vy * delta_t
        self.rect.center = self.x_center, self.y_center

        # Проверка коллизий
        is_collided = False
        for group in self.enemy_collide_groups:
            if sprite := pg.sprite.spritecollideany(self, group):
                is_collided = True
                self.move_back(sprite.rect.center)
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

    def update_room_graph(self, room_graph: dict[tuple[int, int]]):
        """
        Обновление графа комнаты (например, после ломания Poop'a).
        :param room_graph: Графоподобный словарь клеток комнаты.
        """
        self.room_graph = room_graph

    def death(self):
        """
        Смерть врага.
        """
        self.kill()
