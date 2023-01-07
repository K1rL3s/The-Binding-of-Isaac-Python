import pygame as pg

from src.modules.BaseClasses.MovingEnemy import MovingEnemy
from src.modules.BaseClasses.MovableItem import MoveItem


class PickableItem(MoveItem):
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
        MoveItem.__init__(self, xy_pos, collide_groups, *groups,
                          acceleration=acceleration, xy_pixels=xy_pixels)
        self.pick_sound: pg.mixer.Sound | None = None

    def collide(self, other: MoveItem) -> bool:
        """
        Обработка столкновений.

        :param other: С кем было столкновение.
        :return: Было ли столкновение.
        """
        if not MoveItem.collide(self, other):
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
        self.kill()
