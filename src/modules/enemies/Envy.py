import pygame as pg

from src.modules.BaseClasses import MovingEnemy
from src.modules.characters.parents import Body
from src.modules.enemies.fistula import Fistula
from src.utils.funcs import load_sound, load_image, crop


class Envy(Fistula):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [crop(load_image(f'textures/bosses/envy_{i}.png')) for i in range(1, 5)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Body,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 hp_bar_group: pg.sprite.AbstractGroup,
                 stage: int,
                 speed: int | float,
                 *groups: pg.sprite.AbstractGroup):
        Fistula.__init__(self, xy_pos, hp, room_graph, main_hero,
                         enemy_collide_groups, hp_bar_group, stage, speed, *groups)
        self.image = Envy.images[stage - 1]
        self.image = pg.transform.scale2x(self.image)
        self.rect = self.image.get_rect(
            center=(251, 251))

    def death(self):
        MovingEnemy.death(self)
        if self.stage == 4:
            return

        if self.stage == 1:
            Envy((self.x, self.y), 25, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, self.vx + 0.5,
                 *self.groups)
            Envy((self.x, self.y), 25, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, -(abs(self.vx) + 0.5),
                 *self.groups)
        elif self.stage == 2:
            Envy((self.x, self.y), 18, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, self.vx + 0.5,
                 *self.groups)
            Envy((self.x, self.y), 18, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, -(abs(self.vx) + 0.5),
                 *self.groups)
        elif self.stage == 3:
            Envy((self.x, self.y), 10, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, self.vx,
                 *self.groups)
            Envy((self.x, self.y), 10, self.room_graph, self.main_hero,
                 self.enemy_collide_groups, self.hp_bar_group, self.stage + 1, -(abs(self.vx)),
                 *self.groups)
