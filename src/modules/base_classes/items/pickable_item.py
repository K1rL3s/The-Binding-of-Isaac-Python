import pygame as pg

from src.consts import PICKUP_LOOT
from src.modules.base_classes.based.move_sprite import MoveSprite
from src.modules.base_classes.items.base_item import BaseItem
from src.modules.characters.main_hero import Player


class PickableItem(BaseItem):
    """
    Подбираемый предмет.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов.
    :param collidable: Отталкивает ли от себя при столкновении.
    """

    def __init__(
        self,
        xy_pos: tuple[int, int],
        *groups: pg.sprite.AbstractGroup,
        collidable: bool = False,
    ):
        BaseItem.__init__(self, xy_pos, *groups, collidable=collidable)

        self.pick_sound: pg.mixer.Sound | None = None
        self.count: int = 1

    def collide(self, other: MoveSprite) -> bool:
        """
        Обработка столкновений.

        :param other: С кем было столкновение.
        :return: Было ли столкновение.
        """
        if not BaseItem.collide(self, other):
            return False

        # Заменить MovingEnemy на MainCharacter
        if isinstance(other, Player):
            self.pickup()

        return True

    def kill(self):
        if isinstance(self.pick_sound, pg.mixer.Sound):
            self.pick_sound.play()
        MoveSprite.kill(self)

    def pickup(self):
        """
        Подбор предмета.
        В наследователе надо делать pg.event.post(PICKUP_LOOT).
        """
        pg.event.post(
            pg.event.Event(
                PICKUP_LOOT,
                {"item": self, "count": self.count, "self": self},
            ),
        )
