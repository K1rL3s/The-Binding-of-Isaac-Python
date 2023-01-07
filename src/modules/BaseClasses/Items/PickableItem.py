import pygame as pg

from src.consts import PICKUP_LOOT
from src.modules.BaseClasses.Enemies.MovingEnemy import MovingEnemy
from src.modules.BaseClasses.Items.MovableItem import MovableItem


class PickableItem(MovableItem):
    """
    Подбираемый-передвигаемый предмет.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param acceleration: Ускорение торможения в клетках/секунду.
    :param xy_pixels: Позиция в пикселях.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 1,
                 xy_pixels: tuple[int, int] = None):
        MovableItem.__init__(self, xy_pos, collide_groups, *groups,
                             acceleration=acceleration, xy_pixels=xy_pixels)

        self.pick_sound: pg.mixer.Sound | None = None
        self.count: int = 0

    def collide(self, other: MovableItem) -> bool:
        """
        Обработка столкновений.

        :param other: С кем было столкновение.
        :return: Было ли столкновение.
        """
        if not MovableItem.collide(self, other):
            return False

        # Заменить MovingEnemy на MainCharacter
        if isinstance(other, MovingEnemy):
            self.pickup()

        return True

    def pickup(self):
        """
        Подбор предмета.
        В наследователе надо делать pg.event.post(PICKUP_LOOT).
        """
        if isinstance(self.pick_sound, pg.mixer.Sound):
            self.pick_sound.play()
        pg.event.post(pg.event.Event(PICKUP_LOOT, {
                                                  'item': self.__class__,
                                                  'count': self.count,
                                                   }
                                     )
                      )
        self.kill()
