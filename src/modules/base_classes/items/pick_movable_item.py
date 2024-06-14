import pygame as pg

from src.modules.base_classes.items.movable_item import MovableItem
from src.modules.base_classes.items.pickable_item import PickableItem


class PickMovableItem(PickableItem, MovableItem):
    """
    Подбираемый-передвигаемый предмет.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param acceleration: Ускорение торможения в клетках/секунду.
    :param xy_pixels: Позиция в пикселях.
    """

    def __init__(
        self,
        xy_pos: tuple[int, int],
        collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        *groups: pg.sprite.AbstractGroup,
        acceleration: int | float = 1,
        xy_pixels: tuple[int, int] = None,
    ):
        PickableItem.__init__(self, xy_pos, *groups)
        MovableItem.__init__(
            self,
            xy_pos,
            collide_groups,
            *groups,
            acceleration=acceleration,
            xy_pixels=xy_pixels,
        )

    def update(self, delta_t: float):
        PickableItem.update(self, delta_t)
        MovableItem.update(self, delta_t)

    def collide(self, other: MovableItem) -> bool:
        """
        Обработка столкновений.

        :param other: С кем было столкновение.
        :return: Было ли столкновение.
        """
        return bool(
            PickableItem.collide(self, other) + MovableItem.collide(self, other),
        )
