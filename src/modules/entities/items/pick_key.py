import random

import pygame as pg

from src.modules.base_classes import PickMovableItem
from src.utils.funcs import crop, load_image, load_sound

key_width, key_height = 48, 48  # Размеры клетки текстурки


class PickKey(PickMovableItem):
    """
    Класс подбираемого ключа.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    :param count: Количество ключей при подборе.
    """

    keys_images = [
        crop(
            load_image("textures/room/keys.png").subsurface(
                x * key_width,
                0,
                key_width,
                key_height,
            ),
        )
        for x in range(3)
    ]
    pickup_sound = load_sound("sounds/key_pickup.mp3")
    keys: dict[int, tuple[pg.Surface, pg.mixer.Sound]] = {
        1: (keys_images[0], pickup_sound),
        2: (keys_images[1], pickup_sound),
        99: (keys_images[2], load_sound("sounds/key_golden_pickup.mp3")),
    }

    def __init__(
        self,
        xy_pos: tuple[int, int],
        collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        *groups: pg.sprite.AbstractGroup,
        xy_pixels: tuple[int, int] = None,
        count: int = 0,
    ):
        PickMovableItem.__init__(
            self,
            xy_pos,
            collide_groups,
            *groups,
            xy_pixels=xy_pixels,
        )

        self.count = count

        self.set_image()
        self.set_rect()

    def set_image(self):
        if not self.count:
            self.count = random.choices([1, 2, 99], [0.960, 0.035, 0.005])[0]
        self.image, self.pick_sound = PickKey.keys[self.count]
