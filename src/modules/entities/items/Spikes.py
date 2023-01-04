import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image
from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.MoveSprite import MoveSprite


class Spikes(BaseItem):
    """
    Шипы на полу. Бьются.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов.
    :param hiding_delay: С какой задержкой прячется в землю. 0 - не прячется.
    :param hiding_time: На сколько прячется в землю. 0 - навсегда.
    :param colliadble: Наносит ли урон.
    """

    images: list[pg.Surface] = [
        load_image("textures/room/spikes.png").subsurface(
            x * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE
        )
        for x in range(5)
    ]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 hiding_delay: int | float = 0,
                 hiding_time: int | float = 0,
                 colliadble: bool = True):
        BaseItem.__init__(self, xy_pos, *groups, collidable=colliadble)

        self.hiding_delay = hiding_delay
        self.hiding_time = hiding_time
        self.ticks = 0

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = Spikes.images[0]

    def set_rect(self, width: int = None, height: int = None):
        BaseItem.set_rect(self, width, height)
        # Попытаться уменьшить Rect шипов, чтобы края не дамажили (уменьшить текстурку?)

    def hide(self, forever: bool = False):
        """
        Скрыть шипы.

        :param forever: Навсегда ли.
        """
        # Сделать анимацию и звук?
        self.collidable = False
        self.image = Spikes.images[-1]
        if forever:
            self.hiding_time = 0

    def unhide(self):
        """
        Показать шипы.
        """
        # Сделать анимацию и звук?
        self.collidable = True
        self.image = Spikes.images[1]

    def update(self, delta_t: float):
        if not self.hiding_delay:
            return
        self.ticks += delta_t
        if self.ticks >= self.hiding_delay and self.collidable:
            self.ticks = 0
            self.hide()
        if self.ticks >= self.hiding_time and not self.collidable and self.hiding_time:
            self.ticks = 0
            self.unhide()

    def collide(self, other: MoveSprite):
        # Добавить MainCharacter
        if self.collidable and isinstance(other, (BaseEnemy,)):
            other.hurt(1)

