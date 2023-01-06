import random

import pygame as pg

from src.consts import CELL_SIZE, FirePlacesTypes
from src.modules.BaseClasses.BaseTear import BaseTear
from src.modules.BaseClasses.MoveSprite import MoveSprite
from src.utils.funcs import load_image, load_sound
from src.modules.entities.tears.ExampleTear import ExampleTear
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.ShootingEnemy import ShootingEnemy


class FireTextures:
    fires_100 = [
        [
            load_image("textures/room/fireplaces.png").subsurface(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for x in range(6)
        ]
        for y in range(2)
    ]
    fires_67 = [
        [
            pg.transform.scale(
                load_image("textures/room/fireplaces.png").subsurface(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE,
                                                                      CELL_SIZE),
                (CELL_SIZE / 5 * 4, CELL_SIZE / 5 * 4)
            )
            for x in range(6)
        ]
        for y in range(2)
    ]
    fires_33 = [
        [
            pg.transform.scale(
                load_image("textures/room/fireplaces.png").subsurface(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE,
                                                                      CELL_SIZE),
                (CELL_SIZE / 3 * 2, CELL_SIZE / 3 * 2)
            )
            for x in range(6)
        ]
        for y in range(2)
    ]

    fires_wood = [
            (
                load_image("textures/room/firewoods.png").subsurface(x * CELL_SIZE, 0,
                                                                     CELL_SIZE, CELL_SIZE),
                load_image("textures/room/firewoods.png").subsurface(x * CELL_SIZE, CELL_SIZE,
                                                                     CELL_SIZE, CELL_SIZE),
            )
            for x in range(6)
        ]

    fireplace_destoryed = [load_sound("sounds/pop1.wav"), load_sound("sounds/pop2.mp3")]
    fireplace_shot = load_sound("sounds/fire_shot.wav")


class FirePlace(BaseItem, ShootingEnemy, FireTextures):
    """
    Костёр. Бьётся. Ломается.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов.
    :param fire_type: Тип огня.
    :param tear_collide_groups: Группы, с которыми сталкивается слеза костра, если костёр враждебный.
    :param main_hero: Главный герой, если костёр враждебный.
    :param hurtable: Наносит ли урон при касании.
    """

    max_hp = 10

    def __init__(self,
                 xy_pos: tuple[int, int],

                 *groups: pg.sprite.Group,
                 fire_type: FirePlacesTypes = FirePlacesTypes.DEFAULT,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = None,
                 main_hero: pg.sprite.Sprite = None,
                 hurtable: bool = True):
        tear_damage = 1
        tear_distance = 4
        tear_speed = 2
        tear_delay = 7
        tear_class = ExampleTear

        BaseItem.__init__(self, xy_pos, *groups, hurtable=hurtable)
        if fire_type == FirePlacesTypes.RED:
            assert tear_collide_groups and main_hero
            ShootingEnemy.__init__(self, xy_pos, FirePlace.max_hp, FirePlace.max_hp, dict(), main_hero, (),
                                   tear_damage, tear_distance, tear_speed, tear_delay, tear_class, tear_collide_groups,
                                   *groups)

        self.fire_type = fire_type

        self.stages: list[list[pg.Surface]] = [[]]
        self.stage: list[pg.Surface] = []
        self.woods: list[pg.Surface] = []
        self.is_alive = True
        self.ticks = 0
        self.frame = 0
        self.hp = FirePlace.max_hp

        self.set_image()
        self.set_rect()

    def set_image(self):
        y = 0
        for i, fire_type in enumerate(FirePlacesTypes):
            if fire_type == self.fire_type:
                y = i
                break
        self.stages = [FireTextures.fires_100[y], FireTextures.fires_67[y],
                       FireTextures.fires_33[y], [pg.Surface((0, 0))]]
        self.stage = self.stages[0]
        self.woods = random.choice(FireTextures.fires_wood)
        self.update_image()

    def update_image(self):
        self.image = pg.Surface((CELL_SIZE, CELL_SIZE * 1.25), pg.SRCALPHA, 32)
        self.image.blit(self.woods[not self.is_alive], (0, CELL_SIZE * 0.25))
        if self.is_alive:
            self.image.blit(self.stage[self.frame], (
                    (CELL_SIZE - self.stage[0].get_width()) // 2,
                    (CELL_SIZE - self.stage[0].get_height()) // 2
                )
            )

    def update(self, delta_t: float):
        if not self.is_alive:
            return

        if self.fire_type == FirePlacesTypes.RED:
            ShootingEnemy.update(self, delta_t)

        # Сделать это красивее
        self.ticks += delta_t
        if self.ticks > 1 / 15:
            self.ticks = 0
            self.frame = (self.frame + 1) % len(FireTextures.fires_100[0])
            self.update_image()

    def shot(self):
        if ShootingEnemy.shot(self):
            FireTextures.fireplace_shot.play()

    def blow(self):
        """
        Подрыв костра.
        """
        self.hurt(self.hp)

    def hurt(self, damage: int):
        """
        Нанесение урона костру.

        :param damage: Сколько урона.
        """
        if not self.hp:
            return
        self.hp = max(0, self.hp - damage)
        percent = self.hp / FirePlace.max_hp
        self.image = pg.Surface((CELL_SIZE, CELL_SIZE))
        if percent >= 0.67:
            self.stage = self.stages[0]
        elif percent >= 0.33:
            self.stage = self.stages[1]
        elif percent > 0:
            self.stage = self.stages[2]
        else:
            self.destroy()
        if self.hp:
            self.update_image()

    def destroy(self):
        """
        Уничтожение костра после взрыва/поломки.
        """
        self.hurtable = False
        self.is_alive = False
        self.update_image()
        random.choice(self.fireplace_destoryed).play()
        self.drop_loot()

    def draw_tears(self, screen: pg.Surface):
        if self.fire_type == FirePlacesTypes.RED:
            ShootingEnemy.draw_tears(self, screen)

    def collide(self, other: MoveSprite):
        if self.fire_type == FirePlacesTypes.RED and other in self.tears:
            return
        BaseItem.collide(self, other)
        if isinstance(other, BaseTear):
            self.hurt(other.damage)
            other.destroy()

    def drop_loot(self):
        if random.random() > 0.9:
            pass
