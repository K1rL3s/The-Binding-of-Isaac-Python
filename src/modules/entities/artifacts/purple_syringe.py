import pygame as pg

from src.modules.base_classes import BaseArtifact
from src.utils.funcs import load_image


class PurpleSyringe(BaseArtifact):
    """
    Фиолетовый шприц.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/purple_syringe.png")

    mode = BaseArtifact.modes["add"]

    boosts = {"speed": 0.2, "damage": 0.3}

    def __init__(self, xy_pixels: tuple[int, int], *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
