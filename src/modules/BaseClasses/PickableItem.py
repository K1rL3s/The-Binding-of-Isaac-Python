import pygame as pg

from src.consts import PICKUP_LOOT
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.MovingEnemy import MovingEnemy
from src.modules.BaseClasses.MovableItem import MovableItem


class PickableItem(MovableItem):
    """
    Подбираемый-передвигаемый предмет.
    """

    def __init__(self,
                 xy_pos: tuple[int , int],
                 collide_groups: tuple[pg.sprite.AbstractGroup],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 1,
                 xy_pixels: tuple[int, int] = None):
        pickable = True
        super().__init__(xy_pos, collide_groups, *groups,
                         acceleration=acceleration, xy_pixels=xy_pixels, pickable=pickable)

    def collide(self, other: BaseSprite):
        if other == self:
            return

        super().collide(other)
        # Заменить MovingEnemy на MainCharacter
        if isinstance(other, MovingEnemy):
            self.pickup()

    def pickup(self):
        """
        Подбор предмета
        """
        pg.event.post(pg.event.Event(PICKUP_LOOT, {'item': self.__class__}))
        self.kill()

