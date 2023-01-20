import pygame as pg

from src.modules.BaseClasses import BaseSprite, BaseTear, MoveSprite


class Border(BaseSprite):
    """
    Невидимый барьер для стен.

    :param x: Пиксель на экране.
    :param y: Пиксель на экране.
    :param width: Ширина стены.
    :param height: Высота стены.
    :param groups: Группы спрайтов
    :param is_killing: Убивает ли спрайт при коллизии.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 *groups: pg.sprite.AbstractGroup,
                 is_killing: bool = False):
        BaseSprite.__init__(self, (0, 0), *groups)

        self.is_killing = is_killing
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.rect = pg.Rect(x, y, width, height)

        # Для видимости, где это чудо
        #pg.draw.rect(self.image, 'red', (0, 0, self.rect.width, self.rect.height), width=4)

    def collide(self, other: MoveSprite):
        if isinstance(other, BaseTear):
            other.destroy()
        if self.is_killing:
            other.kill()
        else:
            other.move_back(self.rect)

