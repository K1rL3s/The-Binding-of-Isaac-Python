import pygame as pg

from src.modules.base_classes.based.base_sprite import BaseSprite
from src.modules.base_classes.based.base_tear import BaseTear
from src.modules.base_classes.based.move_sprite import MoveSprite


class BaseItem(BaseSprite):
    """
    Базовый класс для предметов (камень, какашка, ключ, монета, артефакт итд).

    :param xy_pos: Позиция в комнате.
    :param groups: Все группы, которым принадлежит предмет-спрайт.
    :param collidable: Можно ли столкнуться с объектом (непроходимый ли).
    :param hurtable: Наносит ли урон персонажу при прикосновении.
    """

    def __init__(
        self,
        xy_pos: tuple[int, int],
        *groups: pg.sprite.AbstractGroup,
        collidable: bool = False,
        hurtable: bool = False,
    ):
        BaseSprite.__init__(self, xy_pos, *groups)

        self.groups = groups
        self.x, self.y = xy_pos
        self.collidable = collidable
        self.hurtable = hurtable

        self.image: pg.Surface
        self.rect: pg.Rect
        self.hp = 0
        self.vx = 0
        self.vy = 0

    def collide(self, other: MoveSprite) -> bool:
        """
        Обработка столкновения с энтити.

        :param other: Объект, с которым прозошло столкновение (персонаж, слеза, взрыв бомбы).
        :return: Произошло ли столкновение.
        """
        if not BaseSprite.collide(self, other):
            return False

        if self.collidable:
            other.move_back(self.rect)
            if isinstance(other, BaseTear):
                other.destroy()
        if self.hurtable:
            other.hurt(1)

        return True

    def destroy(self, *args, **kwargs):
        """
        Разрушение/Удаление энтити.
        """
        # self.kill()
