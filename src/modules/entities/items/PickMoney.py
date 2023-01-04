import random

import pygame as pg

from src.consts import PICKUP_LOOT
from src.modules.BaseClasses.PickableItem import PickableItem
from src.utils.funcs import load_image, load_sound


coin_width, coin_height = 48, 35


class PickMoney(PickableItem):
    """
    Подбираемая монетка (penny, nickel, dime)

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    """

    coins_images = [
        load_image("textures/room/coins.png").subsurface(coin_width * x, 0, coin_width, coin_height)
        for x in range(3)
    ]
    coins: dict[int, tuple[pg.Surface, pg.mixer.Sound]] = {
        1: (coins_images[0], load_sound("sounds/penny_pickup.mp3")),
        5: (coins_images[1], load_sound("sounds/nickel_pickup.mp3")),
        10: (coins_images[2], load_sound("sounds/dime_pickup.mp3"))
    }

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None):
        super().__init__(xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.cost: int = 0
        self.pick_sound: pg.mixer.Sound | None = None
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.cost = random.choices([1, 5, 10], [0.95, 0.045, 0.005])[0]
        self.image, self.pick_sound = PickMoney.coins[self.cost]

    def pickup(self):
        self.pick_sound.play()
        pg.event.post(pg.event.Event(PICKUP_LOOT, {
                                                   'item': self.__class__,
                                                   'cost': self.cost,
                                                  }
                                     )
                      )
        self.kill()
