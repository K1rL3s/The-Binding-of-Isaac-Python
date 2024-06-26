from enum import Enum

import pygame as pg


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
    Возможные направления (x, y) (делать сложение).
    Верхний левый угол — начало координат.
    """

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    TOPLEFT = (-1, -1)
    TOPRIGHT = (1, -1)
    BOTTOMRIGHT = (1, 1)
    BOTTOMLEFT = (-1, 1)


class DoorsCoords(Enum):
    """
    Возможные расположения дверей в комнате (x, y)
    """

    UP = (6, -1)
    DOWN = (6, 7)
    RIGHT = (13, 3)
    LEFT = (-1, 3)


class FirePlacesTypes(Enum):
    """
    Виды костров.
    """

    DEFAULT = "default"
    RED = "red"


class HeartsTypes(Enum):
    """
    Виды сердец персонажа.
    """

    RED = "red"
    BLUE = "blue"
    BLACK = "black"


FPS = 60  # А может 59.98?
WIDTH, HEIGHT = 1280, 960  # Весь экран
GAME_WIDTH, GAME_HEIGHT = 1280, 812  # Часть экрана с игрой
STATS_WIDTH, STATS_HEIGHT = 1280, 148  # Часть экрана с статой (хп, карта, деньги итп)
ROOM_WIDTH, ROOM_HEIGHT = 13, 7  # В клетках
WALL_SIZE = 133  # Размер стены текстурок комнаты (пиксели)
CELL_SIZE = 78  # Размер клетки комнаты (пиксели)
MINIMAP_CELL_WIDTH, MINIMAP_CELL_HEIGHT = 41, 21  # Размер клетки на миникарте
MINIMAP_WIDTH, MINIMAP_HEIGHT = 410, 126  # Размер миникарты (10x6)

MOVE_TO_NEXT_ROOM = pg.USEREVENT + 1  # Переход между комнатами
MOVE_TO_NEXT_LEVEL = pg.USEREVENT + 2  # Переход на следующий этаж
PICKUP_LOOT = pg.USEREVENT + 3  # Подбор лута (бомба, ключ, монета etc)
PICKUP_ART = pg.USEREVENT + 4  # Подбор артефакта
BUY_ITEM = pg.USEREVENT + 5  # Покупка в магазине
USE_BOMB = pg.USEREVENT + 6  # Установка бомбы под персонажем
GAME_OVER = pg.USEREVENT + 7  # Конец игры
GG_HURT = pg.USEREVENT + 8  # ГГ получил урон
USE_KEY = pg.USEREVENT + 9  # Использование ключа для открытия двери
DEATH_ENEMY = pg.USEREVENT + 10  # Враг умер.
