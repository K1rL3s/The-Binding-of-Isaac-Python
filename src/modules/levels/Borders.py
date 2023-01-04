import pygame as pg

from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear


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
        super().__init__(*groups)

        self.is_killing = is_killing
        self.image = pg.Surface((width, height))
        self.rect = pg.Rect(x, y, width, height)

        # Для видимости, где это чудо
        pg.draw.rect(self.image, 'red', (0, 0, self.rect.width, self.rect.height))

    def collide(self, other: BaseSprite):
        if isinstance(other, BaseTear):
            other.destroy()
        if self.is_killing:
            other.kill()
        else:
            other.move_back(self.rect.center)

