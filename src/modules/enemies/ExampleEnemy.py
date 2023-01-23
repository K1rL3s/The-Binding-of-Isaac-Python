import random
from typing import Type

import pygame as pg

from src.modules.BaseClasses import MovingEnemy, ShootingEnemy, BaseTear
from src.modules.entities.tears.ExampleTear import ExampleTear
from src.consts import CELL_SIZE
from src.utils.funcs import load_sound


class ExampleEnemy(MovingEnemy, ShootingEnemy):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 main_hero: pg.sprite.Sprite,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,

                 flyable: bool = False):  # = True чтобы сделать летающим
        hp: int = 10
        speed: int | float = 2
        damage_from_blow: int = 10
        move_update_delay: int | float = 0.1
        shot_damage: int = 1
        shot_max_distance: int | float = 10
        shot_max_speed: int | float = 5
        shot_delay: int | float = 2
        tear_class: Type[BaseTear] = ExampleTear
        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay, room_graph, main_hero,
                             enemy_collide_groups, *groups, flyable=flyable)
        ShootingEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero, enemy_collide_groups,
                               shot_damage, shot_max_distance, shot_max_speed, shot_delay, tear_class,
                               tear_collide_groups, *groups)

        self.set_image()
        self.set_rect()

    def update(self, delta_t: float):
        MovingEnemy.update(self, delta_t)
        ShootingEnemy.update(self, delta_t)

    def set_image(self):
        self.image = pg.Surface((50, 50), pg.SRCALPHA, 32)
        pg.draw.rect(self.image, 'white', (0, 0, 50, 50))

    def move_back(self, rect: pg.Rect):
        MovingEnemy.move_back(self, rect)
        centerx, centery = rect.center
        if (self.rect.centerx < centerx and self.vx > 0) or (self.rect.centerx > centerx and self.vx < 0):
            self.set_speed(0, self.speed if self.vy > 0 else -self.speed)
        if (self.rect.centery > centery and self.vy < 0) or (self.rect.centery < centery and self.vy > 0):
            self.set_speed(self.speed if self.vx > 0 else -self.speed, 0)

    def draw_stats(self, screen: pg.Surface):
        """
        СНИЖАЕТ ФПС!!!
        Пишет скорость над кружком.
        """
        try:
            tear: ExampleTear = self.tears.sprites()[-1]
            t_vx = round(tear.vx / CELL_SIZE, 3)
            t_vy = round(tear.vy / CELL_SIZE, 3)
        except IndexError:
            t_vx = 0
            t_vy = 0
        font = pg.font.Font(None, 25)
        text = font.render(f'{t_vx=}', True, (100, 255, 100))
        text2 = font.render(f'{t_vy=}', True, (100, 255, 100))
        text3 = font.render(f'vx={round(self.vx / CELL_SIZE, 3)}', True, (100, 255, 100))
        text4 = font.render(f'vy={round(self.vy / CELL_SIZE, 3)}', True, (100, 255, 100))
        h = text.get_height()
        text_x = self.rect.x - text.get_width() // 2
        text_y = self.rect.y + text.get_height() - 100
        screen.blit(text, (text_x, text_y))
        screen.blit(text2, (text_x, text_y + h))
        screen.blit(text3, (text_x, text_y + 2 * h))
        screen.blit(text4, (text_x, text_y + 3 * h))

    def death(self):
        random.choice(ExampleEnemy.death_sounds).play()
        MovingEnemy.death(self)
