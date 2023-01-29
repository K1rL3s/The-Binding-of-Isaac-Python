import random
from typing import Type

import pygame as pg

from src.modules.BaseClasses import MovingEnemy, ShootingEnemy, BaseTear
from src.modules.characters.parents import Player
from src.modules.entities.tears.ExampleTear import ExampleTear
from src.utils.funcs import load_sound, load_image


class Maw(MovingEnemy, ShootingEnemy):
    """
    Летающая башка, которая иногда и стреляет.

    :param xy_pos: Позиция в комнате.
    :param main_hero: Главный герой.
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param tear_collide_groups: Группы спрайтов, с которым нужно обрабатывать столкновения слёз.
    :param groups: Группы спрайтов.
    """

    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]

    image = load_image("textures/enemies/maw.png")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        flyable = True
        hp: int = 10
        speed: int | float = 0.75
        damage_from_blow: int = 10
        move_update_delay: int | float = 4
        shot_damage: int = 1
        shot_max_distance: int | float = 4
        shot_max_speed: int | float = 1.25
        shot_delay: int | float = 4
        tear_class: Type[BaseTear] = ExampleTear
        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay, dict(), main_hero,
                             enemy_collide_groups, *groups, flyable=flyable)
        ShootingEnemy.__init__(self, xy_pos, hp, damage_from_blow, dict(), main_hero, enemy_collide_groups,
                               shot_damage, shot_max_distance, shot_max_speed, shot_delay, tear_class,
                               tear_collide_groups, *groups)

        self.set_image()
        self.set_rect()

    def update(self, delta_t: float):
        MovingEnemy.update(self, delta_t)
        ShootingEnemy.update(self, delta_t)

    def set_image(self):
        self.image = Maw.image

    # def move_back(self, rect: pg.Rect):
    #     MovingEnemy.move_back(self, rect)
    #     centerx, centery = rect.center
    #     if (self.rect.centerx < centerx and self.vx > 0) or (self.rect.centerx > centerx and self.vx < 0):
    #         self.set_speed(0, self.speed if self.vy > 0 else -self.speed)
    #     if (self.rect.centery > centery and self.vy < 0) or (self.rect.centery < centery and self.vy > 0):
    #         self.set_speed(self.speed if self.vx > 0 else -self.speed, 0)

    def death(self, is_boss: bool = False):
        random.choice(Maw.death_sounds).play()
        MovingEnemy.death(self)
