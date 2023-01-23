import random

import pygame as pg

from src.modules.BaseClasses import PickMovableItem
from src.consts import HeartsTypes, PICKUP_LOOT
from src.utils.funcs import load_image, load_sound, crop

heart_width, heart_height = 56, 56  # Размеры клетки текстурки


class PickHeart(PickMovableItem):
    """
    Класс подбираемого сердца.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    :param count: Количество сердец при подборе (одна половинка = 1, целое - 2).
    :param heart_type: Тип сердца.
    """

    heart_images = [
        [
            crop(load_image("textures/room/hearts.png").subsurface(x * heart_width, y * heart_height,
                                                                   heart_width, heart_height)
                 )
            for x in range(3)
        ]
        for y in range(3)
    ]
    red_hearts = heart_images[0]
    blue_hearts = heart_images[1]
    black_hearts = heart_images[2]

    pickup_sound = load_sound("sounds/heart_pickup.wav")
    hearts: dict[HeartsTypes, [HeartsTypes, dict[int, tuple[pg.Surface, pg.mixer.Sound]]]] = {
        HeartsTypes.RED: {
            1: (red_hearts[0], pickup_sound),
            2: (red_hearts[1], pickup_sound),
            4: (red_hearts[2], pickup_sound),
        },
        HeartsTypes.BLUE: {
            1: (blue_hearts[0], pickup_sound),
            2: (blue_hearts[1], pickup_sound),
        },
        HeartsTypes.BLACK: {
            1: (black_hearts[0], pickup_sound),
            2: (black_hearts[1], pickup_sound),
        }
    }

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 xy_pixels: tuple[int, int] = None,
                 count: int = 0,
                 heart_type: HeartsTypes = None):
        PickMovableItem.__init__(self, xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.count = count
        self.heart_type = heart_type

        self.set_image()
        self.set_rect()

    def set_image(self):
        if not self.heart_type:
            self.heart_type = random.choices([HeartsTypes.RED, HeartsTypes.BLUE, HeartsTypes.BLACK],
                                             [0.75, 0.20, 0.05])[0]
            if self.heart_type == HeartsTypes.RED:
                self.count = random.choices([1, 2, 4], [0.75, 0.20, 0.05])[0]
            else:
                self.count = random.choices([1, 2], [0.25, 0.75])[0]

        elif not self.count:
            self.heart_type = HeartsTypes.RED
            self.count = random.choices([1, 2, 4], [0.75, 0.20, 0.05])[0]

        self.image, self.pick_sound = PickHeart.hearts[self.heart_type][self.count]

    def pickup(self):
        """
        Подбор предмета.
        """
        pg.event.post(pg.event.Event(PICKUP_LOOT, {
                                                  'item': self,
                                                  'count': self.count,
                                                  'heart_type': self.heart_type,
                                                  'self': self
                                                  }
                                     )
                      )
