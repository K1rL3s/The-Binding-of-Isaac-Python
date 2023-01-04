import pygame as pg

from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.MovableSprite import MovableSprite


class MovableItem(BaseItem, MovableSprite):
    """
    Передвигаемый предмет.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param acceleration: Ускорение торможения в клетках/секунду.
    :param xy_pixels: Позиция в пикселях.
    :param pickable: Можно ли подобрать.
    """

    clear_collide_delay = 1

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 acceleration: int | float = 1,
                 xy_pixels: tuple[int, int] = None,
                 pickable: bool = False):
        BaseItem.__init__(self, xy_pos, *groups, pickable=pickable, movable=True, collidable=False)
        MovableSprite.__init__(self, xy_pos, collide_groups, *groups, acceleration=acceleration, xy_pixels=xy_pixels)

        self.collide_sprites: list[BaseSprite] = []
        self.clear_collide_ticks = 0

    def update(self, delta_t: float):
        self.move(delta_t)
        self.clear_collide_ticks += delta_t
        if self.clear_collide_ticks >= MovableItem.clear_collide_delay:
            self.clear_collide_ticks = 0
            self.collide_sprites.clear()

    def move(self, delta_t: float):
        """
        Перемещение объекта и изменение его скоростей.

        :param delta_t: Время с прошлого кадра.
        """
        MovableSprite.move(self, delta_t)
        MovableSprite.check_collides(self)

    def move_back(self, xy_center: tuple[int, int]):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param xy_center: Центр спрайта, с которым было столкновение
        """
        MovableSprite.move_back(self, xy_center)

        centerx, centery = xy_center
        if self.rect.centerx < centerx and self.vx > 0:
            self.vx = 0
        if self.rect.centerx > centerx and self.vx < 0:
            self.vx = 0
        if self.rect.centery > centery and self.vy < 0:
            self.vy = 0
        if self.rect.centery < centery and self.vy > 0:
            self.vy = 0

    def collide(self, other: MovableSprite):
        """
        Не факт, что работает корректно :)
        Пока что супер примитивно, ага
        """
        if other == self:
            return

        BaseItem.collide(self, other)

        if other not in self.collide_sprites:
            self.collide_sprites.append(other)
            vx = 1 if self.rect.centerx - other.rect.centerx > 0 else -1
            vy = 1 if self.rect.centery - other.rect.centery > 0 else -1
            self.set_speed(self.vx + vx, self.vy + vy)
