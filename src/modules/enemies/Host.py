import math
from typing import Type

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.BaseClasses.Enemies.ShootingEnemy import ShootingEnemy
from src.modules.entities import ExampleTear
from src.modules.characters.parents import Player
from src.utils.funcs import load_image, crop


host_width, host_height = 70, 106


class Host(ShootingEnemy):
    """
    Череп, который вытягивается и стреляет.

    :param xy_pos: Позиция в комнате.
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param tear_collide_groups: Группы спрайтов, с которым нужно обрабатывать столкновения слёз.
    :param groups: Группы спрайтов.
    """

    waiting_image = crop(load_image("textures/enemies/host2.png").subsurface(0, 0, host_width, host_height))
    shooting_image = crop(load_image("textures/enemies/host2.png").subsurface(host_width, 0, host_width, host_height))

    def __init__(self,
                 xy_pos: tuple[int, int],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        hp: int = 10
        damage_from_blow: int = 10
        shot_damage: int = 1
        shot_max_distance: int | float = 5
        shot_max_speed: int | float = 3
        shot_delay: int | float = 4
        tear_class: Type[BaseTear] = ExampleTear
        ShootingEnemy.__init__(self, xy_pos, hp, damage_from_blow, dict(), main_hero, enemy_collide_groups,
                               shot_damage, shot_max_distance, shot_max_speed, shot_delay, tear_class,
                               tear_collide_groups, *groups)

        self.midbottom: tuple[int, int] | None = None
        self.is_shooting = False
        self.set_image()

    def set_image(self):
        if self.is_shooting:
            self.image = Host.shooting_image
        else:
            self.image = Host.waiting_image
        self.set_rect()

    def set_rect(self, width: int | None = None, height: int | None = None, up: int = 0, left: int = 0):
        ShootingEnemy.set_rect(self)
        if self.midbottom:
            self.rect.midbottom = self.midbottom
        else:
            self.midbottom = self.rect.midbottom

    def hurt(self, damage: int):
        if self.is_shooting:
            ShootingEnemy.hurt(self, damage)

    def shot(self):
        # Проверка на расстояние, чтобы не стоял открытым не стреляя.
        x, y = self.main_hero.rect.center
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.shot_max_distance * CELL_SIZE:
            return

        if not self.is_shooting:
            self.is_shooting = True
            self.shot_ticks = self.shot_delay - 1
            self.set_image()
        else:
            ShootingEnemy.shot(self)

    def update(self, delta_t: float):
        if self.is_shooting and self.shot_ticks < 0.5:
            self.is_shooting = False
            self.set_image()
        ShootingEnemy.update(self, delta_t)
