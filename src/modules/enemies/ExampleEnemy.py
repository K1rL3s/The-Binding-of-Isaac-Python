from typing import Type

import pygame as pg

from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.BaseTear import BaseTear
from src.modules.entities.tears.ExampleTear import ExampleTear
from src.consts import CELL_SIZE


class ExampleEnemy(BaseEnemy):
    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 main_hero: pg.sprite.Sprite | BaseEnemy,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 movable: bool = False,
                 flyable: bool = False):
        hp: int = 10
        speed: int | float = 2
        move_delay: int | float = 0.1
        shot_damage: int = 5
        shot_max_distance: int | float = 10
        shot_max_speed: int | float = 5
        shot_delay: int | float = 0
        tear_class: Type[BaseTear] = ExampleTear
        super().__init__(xy_pos, hp, speed, move_delay, room_graph, shot_damage, shot_max_distance, shot_max_speed,
                         shot_delay, tear_class, main_hero, enemy_collide_groups, tear_collide_groups, *groups,
                         movable=movable, flyable=flyable)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = pg.Surface((50, 50), pg.SRCALPHA, 32)
        pg.draw.rect(self.image, 'white', (0, 0, 50, 50))

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
