import pygame as pg


from src.modules.BaseClasses.BaseSprite import BaseSprite
from src.modules.BaseClasses.BaseTear import BaseTear
from src.consts import CELL_SIZE, WALL_SIZE, STATS_HEIGHT


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
        super().__init__(*groups)
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

    def set_rect(self, width: int = None, height: int = None):
        """
        Установка объекта в центре своей клетки.
        """
        self.rect = self.image.get_rect()
        if width:
            self.rect.width = width
        if height:
            self.rect.height = height
        cell_x = self.x * CELL_SIZE + WALL_SIZE + (CELL_SIZE - self.rect.width) // 2
        cell_y = self.y * CELL_SIZE + WALL_SIZE + (CELL_SIZE - self.rect.height) // 2
        if width is None:
            width = self.image.get_width()
        if height is None:
            height = self.image.get_height()
        self.rect = pg.Rect(cell_x, cell_y, width, height)
        self.mask = pg.mask.from_surface(self.image)

    def update(self, delta_t: float):
        """
        Обновление положения объекта (нужно при self.movable = True)

        :param delta_t: Время с прошлого кадра.
        """
        pass

    def pickup(self, *args, **kwargs):
        """
        Подбор предмета (ключ, монета, артефакт)
        """
        pass
        # self.destroy()

    def collide(self, other: BaseSprite):
        """
        Обработка столкновения с энтити.

        :param other: Объект, с которым прозошло столкновение (персонаж, слеза, взрыв бомбы).
        """
        if self.collidable:
            other.move_back(self.rect.center)
        if self.pickable:
            pass
        if self.hurtable:
            other.hurt(1)

    def destroy(self, *args, **kwargs):
        """
        Разрушение/Удаление энтити.
        """
        pass
        # self.kill()
