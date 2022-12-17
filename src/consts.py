from enum import Enum


class RoomsTypes(Enum):
    """
    Константы типов комнат (изменить на какой-нибудь рандом?).
    """
    EMPTY: int = 0
    DEFAULT: int = 1
    SPAWN: int = 2
    TREASURE: int = 3
    SHOP: int = 4
    SECRET: int = 5
    BOSS: int = 6


class Moves(Enum):
    """
    Возможные направления (x, y).
    Верхний левый угол — начало координат.
    """
    UP: tuple[int, int] = (0, -1)
    DOWN: tuple[int, int] = (0, 1)
    RIGHT: tuple[int, int] = (1, 0)
    LEFT: tuple[int, int] = (-1, 0)