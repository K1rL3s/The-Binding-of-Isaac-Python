import pygame as pg

from src.modules.base_classes import BaseArtifact
from src.utils.funcs import load_image


class Dinner(BaseArtifact):
    """
    Обед.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/dinner.png")

    mode = BaseArtifact.modes["add"]

    boosts = {"max_hp": 1}

    def __init__(self, xy_pixels: tuple[int, int], *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
