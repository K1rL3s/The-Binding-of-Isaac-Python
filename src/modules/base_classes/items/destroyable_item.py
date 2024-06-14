import pygame as pg

from src.modules.base_classes.based.base_tear import BaseTear
from src.modules.base_classes.based.move_sprite import MoveSprite
from src.modules.base_classes.items.base_item import BaseItem


class DestroyableItem(BaseItem):
    """
    Ломаемый слезами и бомбами предмет.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов.
    :param collidable: Мешает ли проходу через себя (непроходимый ли).
    :param hurtable: Наносит ли урон при прикосновении.
    """

    def __init__(
        self,
        xy_pos: tuple[int, int],
        *groups: pg.sprite.Group,
        collidable: bool = False,
        hurtable: bool = False,
    ):
        BaseItem.__init__(
            self,
            xy_pos,
            *groups,
            collidable=collidable,
            hurtable=hurtable,
        )

        self.is_alive = True

    def collide(self, other: MoveSprite) -> bool:
        """
        Обработка столкновений.
        :param other: Кто столкнулся.
        :return: Было ли столковение.
        """
        if not self.is_alive or not BaseItem.collide(self, other):
            return False

        if isinstance(other, BaseTear):
            self.hurt(other.damage)
            if not self.collidable:
                other.destroy()

        return True

    def destroy(self):
        """
        Поломка объекта.
        """
        self.collidable = False
        self.hurtable = False
        self.is_alive = False
        self.drop_loot()

    def drop_loot(self):
        """
        Выброс лута после поломки.
        """

    def blow(self):
        """
        Взрыв объекта.
        """
        self.hurt(self.hp)

    def hurt(self, damage: int) -> bool:
        """
        Принятие урона.
        :param damage: Сколько урона.
        :return: Был ли нанесён урон.
        """
        if not self.is_alive:
            return False

        self.hp = max(0, self.hp - damage)

        return True
