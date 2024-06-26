import pygame as pg

from src.modules.base_classes import PickMovableItem
from src.utils.funcs import crop, load_image, load_sound


class PickBomb(PickMovableItem):
    """
    Подбираемая бомба.

    :param xy_pos: Позиция в комнате.
    :param main_hero: Главный герой.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    """

    bomb = crop(load_image("textures/room/bomb.png").subsurface(48, 0, 48, 48))
    pickup_sound = load_sound("sounds/bomb_pickup.wav")

    def __init__(
        self,
        xy_pos: tuple[int, int],
        collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        *groups: pg.sprite.AbstractGroup,
        xy_pixels: tuple[int, int] = None,
    ):
        PickMovableItem.__init__(
            self,
            xy_pos,
            collide_groups,
            *groups,
            xy_pixels=xy_pixels,
        )

        self.count = 1

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = PickBomb.bomb
        self.pick_sound = PickBomb.pickup_sound
