import pygame as pg

from src.modules.BaseClasses.PickableItem import PickableItem
from src.utils.funcs import load_image


class PickMoney(PickableItem):
    """
    Подбираемая монетка (penny, nickel, dime)

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    """

    penny = load_image("textures/room/penny.png")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None):
        super().__init__(xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = PickMoney.penny
