import inspect
import random

import pygame as pg

from src.consts import BUY_ITEM
from src.modules.banners.shop_font import ShopFont
from src.modules.base_classes.based.move_sprite import MoveSprite
from src.modules.base_classes.items.base_artifact import BaseArtifact
from src.modules.base_classes.items.pickable_item import PickableItem


class ShopItem(PickableItem):
    """
    Класс предмета, который можно купить в магазин.

    :param xy_pos: Позиция в комнате.
    :param item: Предмет, который продаётся.
    :param groups: Группы спрайтов.
    :param price: Цена предмета.
    """

    def __init__(
        self,
        xy_pos: tuple[int, int],
        item: type[PickableItem] | type[BaseArtifact],
        *groups: pg.sprite.AbstractGroup,
        price: int = None,
    ):
        PickableItem.__init__(self, xy_pos, *groups, collidable=True)

        assert inspect.isclass(item)

        self.item = item((0, 0), pg.sprite.Group())
        self.font = ShopFont()
        self.event_rect = self.item.rect.copy()

        if price:
            self.price = price
        else:
            if isinstance(self.item, BaseArtifact):
                self.price = 15
            else:
                self.price = random.choice([3, 5, 7, 10, 15])

        self.set_image()
        self.set_rect()
        self.event_rect.center = self.rect.center

    def set_image(self):
        banner = self.font.write_text(f"{self.price}c")
        width = max(self.item.image.get_width(), banner.get_width())
        height = self.item.image.get_height() + banner.get_height()
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.image.blit(
            self.item.image,
            ((width - self.item.image.get_width()) // 2, 0),
        )
        self.image.blit(
            banner,
            ((width - banner.get_width()), (height - banner.get_height())),
        )

    def collide(self, other: MoveSprite):
        """
        Обработка столкновений.

        :param other: С кем было столкновение.
        :return: Было ли столкновение.
        """
        if not pg.Rect.colliderect(self.event_rect, other.rect):
            return
        PickableItem.collide(self, other)

    def kill(self):
        PickableItem.kill(self)
        self.item.kill()

    def pickup(self):
        """
        Подбор (покупка) предмета.
        """
        pg.event.post(
            pg.event.Event(
                BUY_ITEM,
                {
                    "item": self.item,
                    "count": self.count,
                    "heart_type": getattr(self.item, "heart_type", None),
                    "price": self.price,
                    "self": self,
                },
            ),
        )
