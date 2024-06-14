import pygame
import pygame as pg

from src.consts import Moves
from src.modules.banners.boss_hp_bar import BossHPBar, HpBossBarRam
from src.modules.base_classes import MovingEnemy
from src.modules.characters.main_hero import Player
from src.utils.funcs import crop, get_direction, load_image, load_sound


class Fistula(MovingEnemy):
    death_sounds = [load_sound(f"sounds/meat_death{i}.mp3") for i in range(1, 6)]
    images = [crop(load_image(f"textures/bosses/fistula_{i}.png")) for i in range(1, 4)]

    def __init__(
        self,
        xy_pos: tuple[int, int],
        hp: int,
        room_graph: dict[tuple[int, int]],
        main_hero: Player,
        enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        hp_bar_group: pg.sprite.AbstractGroup,
        stage: int,
        speed: int | float,
        *groups: pg.sprite.AbstractGroup,
    ):
        flyable = True
        damage_from_blow: int = 10
        move_update_delay: int | float = 0.1
        MovingEnemy.__init__(
            self,
            xy_pos,
            hp,
            speed,
            damage_from_blow,
            move_update_delay,
            room_graph,
            main_hero,
            enemy_collide_groups,
            *groups,
            flyable=flyable,
        )
        self.room_graph = room_graph
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.hp_bar_group = hp_bar_group
        try:
            self.image = Fistula.images[stage - 1]
            self.image = pygame.transform.scale2x(self.image)
        except IndexError:
            self.image = Fistula.images[stage - 2]
        self.vx = speed
        self.vy = speed
        self.stage = stage
        self.groups = groups
        self.rect = self.image.get_rect(center=(251, 251))  # !!!
        self.hp_bar_ram = HpBossBarRam(hp_bar_group)
        self.hp_bar = BossHPBar(self.hp, hp_bar_group)

    def update(self, delta_t: float):
        MovingEnemy.move(self, delta_t, change_speeds=False)
        MovingEnemy.check_collides(self)

    def move_back(self, rect: pg.Rect):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param rect: Rect того, с чем было столкновение.
        """
        # self.x_center, self.y_center = self.x_center_last, self.y_center_last
        # self.rect.center = self.x_center, self.y_center
        # centerx, centery = rect.center
        # if centerx == GAME_WIDTH - WALL_SIZE and self.vx > 0:
        #     self.vx = -self.vx
        # if centerx == WALL_SIZE and self.vx < 0:
        #     print(123)
        #     self.vx = -self.vx
        # if centery == WALL_SIZE and self.vy < 0:
        #     print(123)
        #     self.vy = -self.vy
        # if centery == GAME_HEIGHT - WALL_SIZE and self.vy > 0:
        #     print(123)
        #     self.vy = -self.vy

        # MovingEnemy.move_back(self, rect)

        direction = get_direction(self.rect, rect)
        if (direction == Moves.DOWN and self.vy > 0) or (
            direction == Moves.UP and self.vy < 0
        ):
            self.vy = -self.vy
        if (direction == Moves.RIGHT and self.vx > 0) or (
            direction == Moves.LEFT and self.vx < 0
        ):
            self.vx = -self.vx

    def hurt(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.death()
        self.hp_bar.hurt(damage)

    def death(self, *args):
        MovingEnemy.death(self, True)
        self.hp_bar.kill()
        self.hp_bar_ram.kill()
        if self.stage == 3:
            return

        if self.stage == 1:
            Fistula(
                (self.x, self.y),
                25,
                self.room_graph,
                self.main_hero,
                self.enemy_collide_groups,
                self.hp_bar_group,
                self.stage + 1,
                self.vx + 0.5,
                *self.groups,
            )
            Fistula(
                (self.x, self.y),
                25,
                self.room_graph,
                self.main_hero,
                self.enemy_collide_groups,
                self.hp_bar_group,
                self.stage + 1,
                -(abs(self.vx) + 0.5),
                *self.groups,
            )
        elif self.stage == 2:
            Fistula(
                (self.x, self.y),
                10,
                self.room_graph,
                self.main_hero,
                self.enemy_collide_groups,
                self.hp_bar_group,
                self.stage + 1,
                self.vx + 0.5,
                *self.groups,
            )
            Fistula(
                (self.x, self.y),
                10,
                self.room_graph,
                self.main_hero,
                self.enemy_collide_groups,
                self.hp_bar_group,
                self.stage + 1,
                -(abs(self.vx) + 0.5),
                *self.groups,
            )
