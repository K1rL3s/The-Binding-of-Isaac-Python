import os
from functools import cache

import pygame as pg

from src.consts import WALL_SIZE, GAME_WIDTH, CELL_SIZE, GAME_HEIGHT


@cache
def load_image(name: str,
               colorkey: pg.Color | int | None = None,
               crop_it: bool = False) -> pg.Surface:
    """
    Загрузка изображения в pygame.Surface.

    :param name: Путь до файла, начиная от src/data, e.g. "textures/room/basement.png"
    :param colorkey: Пиксель, по которому будет удаляться задний фон. Если -1, то по левому верхнему.
    :param crop_it: Обрезать ли изображение по прозрачному фону.
    :return: pygame.Surface
    """
    fullname = os.path.join('src', 'data', name)
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

    if crop_it:
        image = crop(image)

    return image


@cache
def load_sound(name, return_path=False) -> pg.mixer.Sound | str:
    """
    Загрузка звука в pygame.Sound.

    :param name: Путь до файла, начиная от src/data, e.g. "sounds/fart.mp3"
    :param return_path: Вернуть ли путь до файла вместо самого звука.
    :return: pygame.Sound или путь до файла
    """
    fullname = os.path.join('src', 'data', name)
    if not os.path.isfile(fullname):
        exit(f"Файл с звуком '{fullname}' не найден")
    if return_path:
        return fullname
    sound = pg.mixer.Sound(fullname)
    return sound


@cache
def crop(screen: pg.Surface) -> pg.Surface:
    """
    Обрезка изображения по крайним не пустым пикселям.

    :param screen: Изображение.
    :return: Обрезанное изображение.
    """
    pixels = pg.PixelArray(screen)
    background = pixels[0][0]  # noqa
    width, height = screen.get_width(), screen.get_height()
    min_x = width
    min_y = height
    max_x = 0
    max_y = 0

    for x in range(width):
        for y in range(height):
            current = pixels[x][y]  # noqa
            if current != background:
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                min_x = min(x, min_x)
                min_y = min(y, min_y)

    return screen.subsurface((min_x, min_y, max_x - min_x, max_y - min_y))


def pixels_to_cell(xy_pos: tuple[int, int] | tuple[float, float]) -> tuple[int, int] | None:
    """
    Переводит пиксели на экране в клетку комнаты.

    :param xy_pos: Координаты в пикселях.
    :return: Координаты в клетках.
    """
    x, y = xy_pos
    if WALL_SIZE <= x < GAME_WIDTH - WALL_SIZE and WALL_SIZE <= y < GAME_HEIGHT - WALL_SIZE:
        x_cell = x - WALL_SIZE
        y_cell = y - WALL_SIZE
        return int(x_cell // CELL_SIZE), int(y_cell // CELL_SIZE)
    return None


def cell_to_pixels(xy_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Переводит клетку комнаты в пиксели на экране (центр клетки).

    :param xy_pos: Координаты клекти.
    :return: Координаты в пикселях (центр).
    """
    x_cell, y_cell = xy_pos
    x = x_cell * CELL_SIZE + WALL_SIZE + CELL_SIZE // 2
    y = y_cell * CELL_SIZE + WALL_SIZE + CELL_SIZE // 2
    return int(x), int(y)


def cut_sheet(sheet: str | pg.Surface, columns: int, rows: int,
              total: int = None, scale_sizes: tuple[int, int] = None) -> list[pg.Surface]:
    """
    Загрузка шрифта.

    :param sheet: Путь до файла, начиная от src/data, e.g. "font/prices.png" (или сразу Surface).
    :param columns: Количество столбцов.
    :param rows: Количество строк.
    :param total: Сколько всего букв (если есть пустые клетки).
    :param scale_sizes: До каких размеров scale'ить (ширина, высота)
    :return: Список с Surface, где все Surface - число/буква шрифта.
    """

    frames: list[pg.Surface] = []
    if isinstance(sheet, str):
        sheet = load_image(sheet)

    rect = pg.Rect(
        0, 0,
        sheet.get_width() // columns,
        sheet.get_height() // rows
    )

    if scale_sizes:
        scale_sizes = (scale_sizes[0] if scale_sizes[0] != -1 else rect.width,
                       scale_sizes[1] if scale_sizes[0] != -1 else rect.height)

    for y in range(rows):
        if total is not None and len(frames) == total:
            break
        for x in range(columns):
            frame_location = (rect.w * x, rect.h * y)
            part = sheet.subsurface(pg.Rect(frame_location, rect.size))

            if scale_sizes:
                part = pg.transform.scale(part, scale_sizes)

            frames.append(part)

            if total is not None and len(frames) == total:
                break

    return frames
