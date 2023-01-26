import random

import pygame as pg

from src.consts import WALL_SIZE, GAME_WIDTH, GAME_HEIGHT, Moves
from src.modules.Banners.hpboss_bar import HpBossBarRam, HpBossBar
from src.modules.BaseClasses import MovingEnemy
from src.modules.animations.Animation import Animation
from src.modules.characters.parents import Player
from src.modules.enemies.Fly import Fly
from src.utils.funcs import load_sound, load_image, crop, get_direction


class Duke(MovingEnemy):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [crop(load_image(f'textures/bosses/duke_{i}.png')) for i in range(1, 6)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 hp_bar_group: pg.sprite.AbstractGroup,
                 speed: int | float,
                 *groups: pg.sprite.AbstractGroup):  # = True чтобы сделать летающим
        flyable = True
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

        self.animation: Animation | None = None
        self.tear_collide_groups = tear_collide_groups
        self.rect = self.image.get_rect(
            center=(251, 251))
        self.time = 0
        self.rand = random.randint(0, 1)
        self.flag = True

        self.hp_bar_ram = HpBossBarRam(hp_bar_group)
        self.hp_bar = HpBossBar(self.hp, hp_bar_group)

    def update(self, delta_t: float):
        MovingEnemy.move(self, delta_t, change_speeds=False)
        self.time += delta_t
        if self.time >= 3 + self.rand:
            if self.flag:
                self.animation = Animation(Duke.images[1], 2, 1, 60)
                self.image = self.animation.image
            if self.time >= 3.5 + self.rand and self.flag is True:
                self.atak()
                self.flag = False
            elif self.time >= 4 + self.rand:
                self.time = 0
                self.flag = True
                self.rand = random.randint(0, 1)
        else:
            self.image = Duke.images[4]
            self.image = pg.transform.scale2x(self.image)
        # if self.flyable:
        #     MovingEnemy.check_fly_collides(self)
        # else:
        MovingEnemy.check_collides(self)

    def move_back(self, rect: pg.Rect):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param rect: Rect того, с чем было столкновение.
        """
        # self.x_center, self.y_center = self.x_center_last, self.y_center_last
        # self.rect.center = self.x_center, self.y_center
        #
        # centerx, centery = rect.center
        # if centerx == GAME_WIDTH - WALL_SIZE and self.vx > 0:
        #     self.vx = -self.vx
        # if centerx == WALL_SIZE and self.vx < 0:
        #     self.vx = -self.vx
        # if centery == WALL_SIZE and self.vy < 0:
        #     self.vy = -self.vy
        # if centery == GAME_HEIGHT - WALL_SIZE and self.vy > 0:
        #     self.vy = -self.vy

        # MovingEnemy.move_back(self, rect)

        direction = get_direction(self.rect, rect)
        if direction == Moves.DOWN and self.vy > 0:
            self.vy = -self.vy
        elif direction == Moves.UP and self.vy < 0:
            self.vy = -self.vy
        if direction == Moves.RIGHT and self.vx > 0:
            self.vx = -self.vx
        elif direction == Moves.LEFT and self.vx < 0:
            self.vx = -self.vx

    def death(self, *args):
        MovingEnemy.death(self, True)
        self.hp_bar.kill()
        self.hp_bar_ram.kill()
        for i in range(1, random.randint(4, 7)):
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

    def hurt(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.death()
        self.hp_bar.hurt(damage)
