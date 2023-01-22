import pygame as pg

from src.utils.funcs import load_image
from src.modules.BaseClasses import BaseArtifact


class FreshMeat(BaseArtifact):
    """
    Свежее мясо.

    :param xy_pixels: Центр
    """

    image = load_image("textures/artifacts/fresh_meat.png")

    mode = BaseArtifact.modes["add"]  # Метод применения к персонажу (сложение или умножение).

    boosts = {
        "max_hp": 1,
        "heal_hp": 1,
    }

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        BaseArtifact.__init__(self, xy_pixels, *groups)
