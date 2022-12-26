from enum import Enum


class FloorsTypes(Enum):
    """
    Констатны типов этажей.
    """
    BASEMENT: str = "basement"
    CAVES: str = "caves"
    CATACOMBS: str = "catacombs"
    DEPTHS: str = "depths"
    BLUEWOMB: str = "bluewomb"
    WOMB: str = "womb"


class RoomsTypes(Enum):
    """
    Константы типов комнат (изменить на какой-нибудь рандом?).
    """
    EMPTY: str = "empty"
    DEFAULT: str = "default"
    SPAWN: str = "spawn"
    TREASURE: str = "treasure"
    SHOP: str = "shop"
    SECRET: str = "secret"
    BOSS: str = "boss"


class Moves(Enum):
    """
    Возможные направления (x, y).
    Верхний левый угол — начало координат.
    """
    UP: tuple[int, int] = (0, -1)
    DOWN: tuple[int, int] = (0, 1)
    RIGHT: tuple[int, int] = (1, 0)
    LEFT: tuple[int, int] = (-1, 0)


class DoorsCoords(Enum):
    """
    Возможные расположения дверей в комнате (x, y)
    """
    UP = (6, -1)
    DOWN = (6, 7)
    LEFT = (-1, 3)
    RIGHT = (13, 3)


WIDTH, HEIGHT = 1280, 960                # Весь экран
GAME_WIDTH, GAME_HEIGHT = 1280, 810      # Часть экрана с игрой
STATS_WIDTH, STATS_HEIGHT = 1280, 150    # Часть экрана с статой (хп, карта, деньги итп)
ROOM_WIDTH, ROOM_HEIGHT = 13, 7          # В клетках
WALL_SIZE = 133                          # Размер стены текстурок комнаты (пиксели)
CELL_SIZE = 78                           # Размер клетки комнаты (пиксели)

