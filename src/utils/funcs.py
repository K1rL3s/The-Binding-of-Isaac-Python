import os
from functools import cache

import pygame as pg


@cache
def load_image(name: str, colorkey: pg.Color | int | None = None) -> pg.Surface:
    """
    Загрузка изображения в pygame.Surface.

    :param name: Путь до файла, начиная от src/data, e.g. "textures/room/basement.png"
    :param colorkey: Пиксель, по которому будет удаляться задний фон. Если -1, то по левому верхнему.
    :return: pygame.Surface
    """
    fullname = os.path.join('src', 'data', name.replace('/', '\\'))
    if not os.path.isfile(fullname):
        exit(f"Файл с изображением '{fullname}' не найден")
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


@cache
def load_sound(name) -> pg.mixer.Sound:
    """
    Загрузка звука в pygame.Sound.

    :param name: Путь до файла, начиная от src/data, e.g. "sounds/fart.mp23"
    :return: pygame.Sound
    """
    fullname = os.path.join('src', 'data', name.replace('/', '\\'))
    if not os.path.isfile(fullname):
        exit(f"Файл с звуком '{fullname}' не найден")
    sound = pg.mixer.Sound(fullname)
    return sound
