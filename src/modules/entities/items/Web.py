import random

import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.MovingEnemy import MovingEnemy
from src.modules.BaseClasses.MovableItem import MoveItem
from src.modules.BaseClasses.MoveSprite import MoveSprite


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

    slowdown_coef = 3/4
    clear_collides_delay = 1

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 colliadble: bool = True):
        BaseItem.__init__(self, xy_pos, *groups, collidable=colliadble)

        self.collide_sprites: list[MoveSprite] = []
        self.ticks = 0

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = random.choice(Web.webs)

    def blow(self):
        """
        Взрыв (поломка) паутины.
        """
        self.collidable = False
        self.image = Web.destoryed
        self.reset_collides_sprites()

    def update(self, delta_t: float):
        self.ticks += delta_t
        if self.ticks >= Web.clear_collides_delay:
            self.ticks = 0
            self.reset_collides_sprites()

    def reset_collides_sprites(self):
        """
        Обнуление списка столкновений и возврат коэфициента скорости.
        """
        for sprite in self.collide_sprites:
            sprite: MoveSprite
            sprite.slowdown_coef = 1
        self.collide_sprites.clear()

    def collide(self, other: MoveSprite):
        # Изменить MovingEnemy на MainCharacter или просто добавить MainCharacter?
        # Работает уже лучше, потому что коэф есть, но он с задержкой убирается,
        # можно сделать Web.clear_collides_delay меньше.
        if self.collidable and isinstance(other, (MovingEnemy, MoveItem)):
            if other not in self.collide_sprites:
                self.collide_sprites.append(other)
                other.slowdown_coef = Web.slowdown_coef
