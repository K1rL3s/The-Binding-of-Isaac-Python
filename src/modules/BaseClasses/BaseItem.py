import pygame as pg


from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear
from src.modules.BaseClasses.MovableSprite import MovableSprite


class BaseItem(BaseSprite):
    """
    Базовый класс для предметов (камень, какашка, ключ, монета, артефакт итд).

    :param xy_pos: Позиция в комнате.
    :param groups: Все группы, которым принадлежит предмет-спрайт.
    :param colliadble: Можно ли столкнуться с объектом (непроходимый ли).
    :param destroyable: Можно ли сломать слезой.
    :param pickable: Можно ли подобрать.
    :param movable: Двигается ли после взрыва бомбы или толчка игроком.
    :param hurtable: Наносит ли урон персонажу при прикосновении.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = False,
                 destroyable: bool = False,
                 pickable: bool = False,
                 movable: bool = False,
                 hurtable: bool = False):
        BaseSprite.__init__(self, xy_pos, *groups)
        self.groups = groups

        self.x, self.y = xy_pos
        self.collidable = collidable
        self.destroyable = destroyable
        self.pickable = pickable
        self.movable = movable
        self.hurtable = hurtable

        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))
        self.hp = 0
        self.vx = 0
        self.vy = 0

    def collide(self, other: MovableSprite):
        """
        Обработка столкновения с энтити.

        :param other: Объект, с которым прозошло столкновение (персонаж, слеза, взрыв бомбы).
        """
        if other == self:
            return

        if self.collidable:
            other.move_back(self.rect.center)
            if isinstance(other, BaseTear):
                other.destroy()
        if self.hurtable:
            other.hurt(1)

    def destroy(self, *args, **kwargs):
        """
        Разрушение/Удаление энтити.
        """
        pass
        # self.kill()
