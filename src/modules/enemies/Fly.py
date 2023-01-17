import random
from typing import Type

import pygame as pg

from src.modules.BaseClasses import MovingEnemy, ShootingEnemy, BaseTear
from src.modules.entities.tears.ExampleTear import ExampleTear
from src.modules.characters.parents import Player
from src.utils.funcs import load_image
from src.modules.animations.Animation import Animation


class Fly(MovingEnemy, ShootingEnemy):
    fly_ok = load_image("textures/enemy/fly_ok.png")
    fly_ne_ok = load_image("textures/enemy/fly_ne_ok.png")
    fly_shoot = load_image("textures/enemy/fly_shoot.png")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        hp: int = 10000
        speed: int | float = 1
        damage_from_blow: int = 10000
        move_update_delay: int | float = 1
        shot_damage: int = 1
        shot_max_distance: int | float = 5
        shot_max_speed: int | float = 1.5
        shot_delay: int | float = 3
        tear_class: Type[BaseTear] = ExampleTear
        flyable: bool = True
        self.angry = random.random() > 0.5
        self.shooting = random.random()
        if self.angry:
            if self.shooting > 0.5:
                self.sheet = Fly.fly_shoot
                self.animation = Animation(self.sheet, 2, 1, 30)
            else:
                self.sheet = Fly.fly_ne_ok
                self.animation = Animation(self.sheet, 4, 1, 30)
                self.shooting = False
        else:
            self.sheet = Fly.fly_ok
            self.animation = Animation(self.sheet, 4, 1, 30)
            self.shooting = False

        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay, room_graph, main_hero,
                             enemy_collide_groups, *groups, flyable=flyable)
        ShootingEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero,
                               enemy_collide_groups, shot_damage, shot_max_distance, shot_max_speed,
                               shot_delay, tear_class, tear_collide_groups, *groups)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = self.animation.image

    def update(self, delta_t):
        MovingEnemy.update(self, delta_t)
        if self.shooting:
            ShootingEnemy.update(self, delta_t)
        self.animation.update(delta_t)
        self.image = self.animation.image

    def update_move_speed(self):
        if self.angry:
            MovingEnemy.update_move_speed(self)
        else:
            self.vx = random.uniform(-self.speed, self.speed)
            self.vy = random.uniform(-self.speed, self.speed)
