import random

import pygame as pg

from src.modules.BaseClasses import MovingEnemy
from src.modules.animations.Animation import Animation
from src.modules.characters.parents import Player
from src.modules.enemies.Fly import Fly
from src.utils.funcs import load_sound, load_image, crop


class Duke(MovingEnemy):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [crop(load_image(f'textures/bosses/duke_{i}.png')) for i in range(1, 6)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 speed: int | float,
                 *groups: pg.sprite.AbstractGroup,
                 flyable: bool = False):  # = True чтобы сделать летающим
        hp: int = 40
        damage_from_blow: int = 10
        move_update_delay: int | float = 0.1
        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay, room_graph, main_hero,
                             enemy_collide_groups, *groups, flyable=flyable)
        self.hp = hp
        self.room_graph = room_graph
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.image = Duke.images[0]
        self.image = pg.transform.scale2x(self.image)
        self.vx = speed
        self.vy = speed
        self.groups = groups
        self.time = 0
        self.tear_collide_groups = tear_collide_groups
        self.rect = self.image.get_rect(
            center=(251, 251))
        self.rand = self.time >= 5 + random.randint(-1, 1)
        self.flag = True

    def update(self, delta_t: float):
        MovingEnemy.move(self, delta_t, change_speeds=False)
        self.time += delta_t
        if self.time >= 4.5 + self.rand:
            if self.flag:
                self.animation = Animation(Duke.images[1], 2, 1, 60)
                self.image = self.animation.image
            if self.time >= 5 + self.rand and self.flag is True:
                self.atak()
                self.flag = False
            elif self.time >= 5.5 + self.rand:
                self.time = 0
                self.flag = True
        else:
            self.image = Duke.images[4]
            self.image = pg.transform.scale2x(self.image)
        if self.flyable:
            MovingEnemy.check_fly_collides(self)
        else:
            MovingEnemy.check_collides(self)


    def death(self):
        MovingEnemy.death(self)
        for i in range(1, random.randint(3, 5)):
            Fly((self.x, self.y), self.room_graph, self.main_hero,
                self.enemy_collide_groups,
                self.tear_collide_groups,
                *self.groups)

    def atak(self):
        self.image = Duke.images[3]
        self.image = pg.transform.scale2x(self.image)
        Fly((self.x, self.y), self.room_graph, self.main_hero,
            self.enemy_collide_groups,
            self.tear_collide_groups,
            *self.groups)
