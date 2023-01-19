import pygame as pg

from src.modules.BaseClasses import MovingEnemy
from src.modules.characters.parents import Player
from src.modules.enemies.fistula import Fistula
from src.utils.funcs import load_sound, load_image, crop


class Teratoma(Fistula):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [crop(load_image(f'textures/bosses/teratoma_{i}.png')) for i in range(1, 4)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 stage: int,
                 speed: int | float,
                 *groups: pg.sprite.AbstractGroup,
                 flyable: bool = False):  # = True чтобы сделать летающим
        damage_from_blow: int = 10
        move_update_delay: int | float = 0.1
        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay, room_graph, main_hero,
                             enemy_collide_groups, *groups, flyable=flyable)
        self.room_graph = room_graph
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.image = Teratoma.images[stage - 1]
        self.image = pg.transform.scale2x(self.image)
        self.vx = speed
        self.vy = speed
        self.stage = stage
        self.groups = groups
        self.rect = self.image.get_rect(
            center=(251, 251))

    def death(self):
        MovingEnemy.death(self)
        if self.stage == 3:
            # НАДО СДЕЛАТЬ ЛЮК!!!
            return 0
        if self.stage == 1:
            Teratoma((self.x, self.y), 25, self.room_graph, self.main_hero,
                     (self.enemy_collide_groups[0],), self.stage + 1, self.vx + 0.5,
                     *self.groups, flyable=True)
            Teratoma((self.x, self.y), 25, self.room_graph, self.main_hero,
                     (self.enemy_collide_groups[0],), self.stage + 1, -(abs(self.vx) + 0.5),
                     *self.groups, flyable=True)
        if self.stage == 2:
            Teratoma((self.x, self.y), 10, self.room_graph, self.main_hero,
                     (self.enemy_collide_groups[0],), self.stage + 1, self.vx + 0.5,
                     *self.groups, flyable=True)
            Teratoma((self.x, self.y), 10, self.room_graph, self.main_hero,
                     (self.enemy_collide_groups[0],), self.stage + 1, -(abs(self.vx) + 0.5),
                     *self.groups, flyable=True)
