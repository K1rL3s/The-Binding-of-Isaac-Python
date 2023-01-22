import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class WhiteSyringe(BaseArtifact):
    """
    Белый шприц.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/white_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {
        "speed": 0.2,
        "shot_speed": 0.3,
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
