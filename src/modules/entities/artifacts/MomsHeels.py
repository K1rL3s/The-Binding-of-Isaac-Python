import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class MomsHeels(BaseArtifact):
    """
    Мамины туфли.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/moms_heels.png")

    mode = BaseArtifact.modes["add"]

    boosts = {
        "shot_distance": 2
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
