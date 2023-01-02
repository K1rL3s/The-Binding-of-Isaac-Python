from typing import Type
import math

import pygame as pg

from src.utils.funcs import cell_to_pixels, load_sound
from src.consts import CELL_SIZE, WALL_SIZE
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear


class BaseEnemy(BaseSprite):
    """
    Базовый класс противника.

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param damage_from_blow: Урон получаемый от взрывов.
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

    explosion_kill = load_sound("sounds/explosion_kill.mp3")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
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
        self.damage_from_blow = damage_from_blow
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

        self.x_center, self.y_center = cell_to_pixels(xy_pos)
        self.x_center_last, self.y_center_last = self.x_center, self.y_center
        self.path: list[tuple[int, int]] = []
        self.shot_ticks = 0
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

        if self.shot_ticks >= self.shot_delay:
            self.shot()

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
        cell_y = self.y * CELL_SIZE + WALL_SIZE + (CELL_SIZE - self.rect.width) // 2
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

    def blow(self):
        """
        Взрыв сущности.
        """
        self.hurt(self.damage_from_blow)
        if self.hp <= 0:
            BaseEnemy.explosion_kill.play()

    def hurt(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.death()

    def shot(self):
        """
        Выстрел в сторону ГГ.
        """
        self.shot_ticks = 0
        x, y = self.main_hero.rect.center
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE or distance == 0:  # Стреляет тогда, когда уже вплотную, ну хз.
            return
        vx = self.shot_max_speed * dx / distance
        vy = self.shot_max_speed * dy / distance
        self.tear_class(self.rect.center, self.shot_damage, self.shot_max_distance, vx, vy,
                        self.tear_collide_groups, self.tears)

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
