import pygame as pg

from src.modules.BaseClasses.PickableItem import PickableItem
from src.utils.funcs import load_image, load_sound, crop
from src.consts import PICKUP_LOOT


class PickBomb(PickableItem):
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

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None):
        super().__init__(xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = PickBomb.bomb

    def pickup(self):
        """
        Подбор бомбы.
        """
        PickBomb.pickup_sound.play()
        pg.event.post(pg.event.Event(PICKUP_LOOT, {'item': PickBomb}))
        self.kill()

