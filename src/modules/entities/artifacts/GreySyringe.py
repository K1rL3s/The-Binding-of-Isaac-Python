import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class GreySyringe(BaseArtifact):
    """
    Серый шприц.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/grey_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {
        "damage": 0.3,
        "shot_distance": 1
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
