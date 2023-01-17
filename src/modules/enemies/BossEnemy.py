import pygame as pg

from src.consts import WALL_SIZE, GAME_WIDTH, GAME_HEIGHT
from src.modules.BaseClasses import MovingEnemy
from src.modules.characters.parents import Player
from src.utils.funcs import load_sound, load_image


class BossEnemy(MovingEnemy):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [load_image(f'textures/bosses/teratoma_{i}.png') for i in range(1, 4)]

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
        self.image = BossEnemy.images[stage - 1]
        self.image = pg.transform.scale2x(self.image)
        self.vx = speed
        self.vy = speed
        self.stage = stage
        self.groups = groups
        self.rect = self.image.get_rect(
            center=(251, 251))

    def update(self, delta_t: float):
        MovingEnemy.move(self, delta_t, change_speeds=False)
        if self.flyable:
            MovingEnemy.check_fly_collides(self)
        else:
            MovingEnemy.check_collides(self)

    def move_back(self, rect: pg.Rect):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param rect: Rect того, с чем было столкновение.
        """
        self.x_center, self.y_center = self.x_center_last, self.y_center_last
        self.rect.center = self.x_center, self.y_center

        centerx, centery = rect.center
        if centerx == GAME_WIDTH - WALL_SIZE and self.vx > 0:
            self.vx = -self.vx
        if centerx == WALL_SIZE and self.vx < 0:
            self.vx = -self.vx
        if centery == WALL_SIZE and self.vy < 0:
            self.vy = -self.vy
        if centery == GAME_HEIGHT - WALL_SIZE and self.vy > 0:
            self.vy = -self.vy

    def death(self):
        MovingEnemy.death(self)
        if self.stage == 3:
            # НАДО СДЕЛАТЬ ЛЮК!!!
            return 0
        if self.stage == 1:
            BossEnemy((self.x, self.y), 25, self.room_graph, self.main_hero,
                      (self.enemy_collide_groups[0],), self.stage + 1, self.vx + 0.5,
                      *self.groups, flyable=True)
            BossEnemy((self.x, self.y), 25, self.room_graph, self.main_hero,
                      (self.enemy_collide_groups[0],), self.stage + 1, -(abs(self.vx) + 0.5),
                      *self.groups, flyable=True)
        if self.stage == 2:
            BossEnemy((self.x, self.y), 10, self.room_graph, self.main_hero,
                      (self.enemy_collide_groups[0],), self.stage + 1, self.vx + 0.5,
                      *self.groups, flyable=True)
            BossEnemy((self.x, self.y), 10, self.room_graph, self.main_hero,
                      (self.enemy_collide_groups[0],), self.stage + 1, -(abs(self.vx) + 0.5),
                      *self.groups, flyable=True)
