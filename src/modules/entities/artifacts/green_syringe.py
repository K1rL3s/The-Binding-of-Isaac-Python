import pygame as pg

from src.modules.base_classes import BaseArtifact
from src.utils.funcs import load_image


class GreenSyringe(BaseArtifact):
    """
    Зеленый шприц.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/green_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {"speed": 0.2, "shot_distance": 1}

    def __init__(self, xy_pixels: tuple[int, int], *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
