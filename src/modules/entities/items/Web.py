import random

import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.MovingEnemy import MovingEnemy
from src.modules.BaseClasses.MovableItem import MovableItem


class Web(BaseItem):
    """
    Класс паутинки, которая замедляет.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов.
    :param colliadble: Замедляет ли.
    """

    webs: list[pg.Surface] = [load_image("textures/room/web.png").subsurface(x * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
                              for x in range(3)]
    destoryed: pg.Surface = load_image("textures/room/web.png").subsurface(3 * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
    slowdown_coef = 4 / 5

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 colliadble: bool = True):
        super().__init__(xy_pos, *groups, collidable=colliadble)

        self.collide_sprites: list[BaseSprite] = []
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = random.choice(Web.webs)

    def blow(self):
        self.collidable = False
        self.image = Web.destoryed

    def collide(self, other: BaseSprite):
        # Изменить MovingEnemy на MainCharacter или просто добавить MainCharacter?
        # Работает не очень норм, потому что скорости MovingEnemy обновляются сами и это не фиксирует паутина
        temp_collides: list[BaseSprite] = []
        if self.collidable and isinstance(other, (MovingEnemy, MovableItem)):
            temp_collides.append(other)
            if other not in self.collide_sprites:
                other.set_speed(other.vx * Web.slowdown_coef, other.vy * Web.slowdown_coef)
        self.collide_sprites = temp_collides
