import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class FreshMeat(BaseArtifact):
    """
    Свежее мясо.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/fresh_meat.png")

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
