import os
import sqlite3
import sys
from functools import cache

import pygame as pg

from src.consts import CELL_SIZE, GAME_HEIGHT, GAME_WIDTH, WALL_SIZE, Moves


def resource_path(*relative_path, use_abs_path: bool = False):
    save_relative = relative_path

    if not use_abs_path and getattr(sys, "_MEIPASS", False):
        base_path = sys._MEIPASS
        relative_path = relative_path[2:]
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path), save_relative, relative_path


@cache
def load_image(
    name: str,
    colorkey: pg.Color | int | None = None,
    crop_it: bool = False,
) -> pg.Surface:
    """
    Загрузка изображения в pygame.Surface.

    :param name: Путь до файла, начиная от src/data, e.g. "textures/room/basement.png"
    :param colorkey: Пиксель, по которому будет удаляться задний фон. Если -1, то по левому верхнему.
    :param crop_it: Обрезать ли изображение по прозрачному фону.
    :return: pygame.Surface
    """
    fullname, save_rel, rel = resource_path("src", "data", *name.split("/"))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(
            f"Файл с изображением '{fullname}' не найден\n{save_rel}\n{rel}",
        )
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
def load_sound(name, return_path: bool = False) -> pg.mixer.Sound | str:
    """
    Загрузка звука в pygame.Sound.

    :param name: Путь до файла, начиная от src/data, e.g. "sounds/fart.mp3"
    :param return_path: Вернуть ли путь до файла вместо самого звука.
    :return: pygame.Sound или путь до файла
    """
    fullname, save_rel, rel = resource_path("src", "data", *name.split("/"))
    if not os.path.isfile(fullname):
        raise FileNotFoundError(
            f"Файл с звуком '{fullname}' не найден\n{save_rel}\n{rel}",
        )
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
    background = pixels[0][0]
    width, height = screen.get_width(), screen.get_height()
    min_x = width
    min_y = height
    max_x = 0
    max_y = 0

    for x in range(width):
        for y in range(height):
            current = pixels[x][y]
            if current != background:
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                min_x = min(x, min_x)
                min_y = min(y, min_y)

    return screen.subsurface((min_x, min_y, max_x - min_x, max_y - min_y))


def pixels_to_cell(
    xy_pos: tuple[int, int] | tuple[float, float],
) -> tuple[int, int] | None:
    """
    Переводит пиксели на экране в клетку комнаты.

    :param xy_pos: Координаты в пикселях.
    :return: Координаты в клетках.
    """
    x, y = xy_pos
    if (
        WALL_SIZE <= x < GAME_WIDTH - WALL_SIZE
        and WALL_SIZE <= y < GAME_HEIGHT - WALL_SIZE
    ):
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


def cut_sheet(
    sheet: str | pg.Surface,
    columns: int,
    rows: int,
    total: int = None,
    scale_sizes: tuple[int, int] = None,
) -> list[pg.Surface]:
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

    rect = pg.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

    if scale_sizes:
        scale_sizes = (
            scale_sizes[0] if scale_sizes[0] != -1 else rect.width,
            scale_sizes[1] if scale_sizes[0] != -1 else rect.height,
        )

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


def get_direction(second_rect: pg.Rect, first_rect: pg.Rect):
    """
    Возвращает, с какой стороны второй rect

    :param first_rect: тело, которое врезалось
    :param second_rect: тело, с которым произошло столкновение
    """
    if (
        first_rect.collidepoint(second_rect.midright)
        and (
            first_rect.collidepoint(second_rect.topright)
            or first_rect.collidepoint(second_rect.bottomright)
        )
        and not first_rect.collidepoint(second_rect.midleft)
        and (
            not first_rect.collidepoint(second_rect.topleft)
            or not first_rect.collidepoint(second_rect.bottomleft)
        )
    ):
        return Moves.RIGHT

    if (
        first_rect.collidepoint(second_rect.midleft)
        and (
            first_rect.collidepoint(second_rect.topleft)
            or first_rect.collidepoint(second_rect.bottomleft)
        )
        and not first_rect.collidepoint(second_rect.midright)
        and (
            not first_rect.collidepoint(second_rect.topright)
            or not first_rect.collidepoint(second_rect.bottomright)
        )
    ):
        return Moves.LEFT

    if (
        first_rect.collidepoint(second_rect.midbottom)
        and (
            first_rect.collidepoint(second_rect.bottomleft)
            or first_rect.collidepoint(second_rect.bottomright)
        )
        and not first_rect.collidepoint(second_rect.midtop)
        and (
            not first_rect.collidepoint(second_rect.topleft)
            or not first_rect.collidepoint(second_rect.topright)
        )
    ):
        return Moves.DOWN

    if (
        first_rect.collidepoint(second_rect.midtop)
        and (
            first_rect.collidepoint(second_rect.topleft)
            or first_rect.collidepoint(second_rect.topright)
        )
        and not first_rect.collidepoint(second_rect.midbottom)
        and (
            not first_rect.collidepoint(second_rect.bottomleft)
            or not first_rect.collidepoint(second_rect.bottomright)
        )
    ):
        return Moves.UP

    first_rect, second_rect = second_rect, first_rect

    if second_rect.collidepoint(first_rect.topleft):
        return Moves.TOPLEFT

    if second_rect.collidepoint(first_rect.topright):
        return Moves.TOPRIGHT

    if second_rect.collidepoint(first_rect.bottomleft):
        return Moves.BOTTOMLEFT

    if second_rect.collidepoint(first_rect.bottomright):
        return Moves.BOTTOMRIGHT


def create_data_base():
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS game_over (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_or_loose STRING,
            score INT);
            """,
    )
    con.commit()


def add_db(win_or_loose: str, score: int):
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    cur.execute(
        """INSERT INTO game_over (win_or_loose, score) VALUES (?, ?)""",
        (win_or_loose, score),
    )
    con.commit()


def select_from_db():
    con = sqlite3.connect(resource_path("stats.sqlite", use_abs_path=True)[0])
    cur = con.cursor()
    res = cur.execute("""SELECT * FROM game_over""").fetchall()
    return res
