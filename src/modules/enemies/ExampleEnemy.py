from typing import Type

import pygame as pg

from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.BaseTear import BaseTear
from src.modules.entities.tears.ExampleTear import ExampleTear


class ExampleEnemy(BaseEnemy):
    def __init__(self,
                 xy_pos: tuple[int, int],
                 main_hero: pg.sprite.Sprite | BaseEnemy,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 hp: int = 10,
                 speed: int | float = 1,
                 shot_damage: int | float = 1,
                 shot_max_distance: int | float = 5,
                 shot_max_speed: int | float = 5,
                 shot_delay: int | float = 0,
                 tear_class: Type[BaseTear] = ExampleTear,
                 movable: bool = False,
                 flyable: bool = False):
        super().__init__(xy_pos, hp, speed, shot_damage, shot_max_distance, shot_max_speed, shot_delay,
                         tear_class, main_hero, collide_groups, *groups, movable=movable, flyable=flyable)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = pg.Surface((50, 50), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, 'white', (25, 25), 25)

    def draw_stats(self, screen: pg.Surface):
        """
        Пишет скорость над кружком.
        """
        try:
            tear: ExampleTear = self.tears.sprites()[-1]
        except IndexError:
            return
        font = pg.font.Font(None, 25)
        text = font.render(f'{round(tear.vx, 3)}', True, (100, 255, 100))
        text2 = font.render(f'{round(tear.vy, 3)}', True, (100, 255, 100))
        text_x = self.rect.x - text.get_width() // 2
        text_y = self.rect.y + text.get_height() - 50
        screen.blit(text, (text_x, text_y))
        screen.blit(text2, (text_x, text_y + text2.get_height()))

