import random

import pygame as pg

import xml.etree.ElementTree as XMLTree

from src import consts
from src.modules.entities.Rock import Rock
from src.utils.graph import make_neighbors_graph


class Room:
    """
    Класс комнаты.

    :param floor_type: Номер этажа (1-5).
    :param room_type: Тип комнаты.
    :param texture_variant: Вариант текстуры (1-4, один из вариантов из изображения).
    :param abs_pos: Расположение на всей карте (x, y).
    :param xml_description: XML разметка объектов в комнате.
    :param all_textures: Все текстуры игры.
    :param all_sounds: Все звуки игры.
    """

    def __init__(self, floor_type: consts.FloorsTypes | str,
                 room_type: consts.RoomsTypes | int,
                 texture_variant: int,
                 abs_pos: tuple[int, int],
                 xml_description: XMLTree,
                 all_textures: dict[str, dict[consts.FloorsTypes | consts.RoomsTypes | str, pg.Surface]],
                 all_sounds: dict[str, pg.mixer.Sound | list[pg.mixer.Sound]]):

        self.x, self.y = abs_pos
        self.floor_type = floor_type
        self.room_type = room_type
        self.texture_variant = texture_variant
        self.all_textures = all_textures
        self.all_sounds = all_sounds
        self.background = pg.Surface((0, 0))

        # Отображение на мини-карте разными цветами
        self.visited = False
        self.spotted = False
        
        # Анимация входа-выхода
        self.moving = False

        self.all_obstacles = pg.sprite.Group()
        self.colliadble_group = pg.sprite.Group()
        self.destroyable_group = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.poops = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.other = pg.sprite.Group()  # Бомбы, ключи, монеты итд итп
        self.paths = dict()  # Пути для наземных
        self.fly_paths = dict()  # Пути для летающих врагов

        self.setup_background()
        self.setup_entities(xml_description)
        self.update_obstacles()
        self.setup_graph()

    def setup_background(self):
        texture_x = texture_y = 0
        if self.texture_variant == 2:
            texture_x = consts.GAME_WIDTH // 2
        elif self.texture_variant == 3:
            texture_y = consts.GAME_HEIGHT // 2
        elif self.texture_variant == 4:
            texture_x = consts.GAME_WIDTH // 2
            texture_y = consts.GAME_WIDTH // 2

        if self.room_type in (consts.RoomsTypes.TREASURE, consts.RoomsTypes.SHOP, consts.RoomsTypes.SECRET):
            texture = self.all_textures["rooms"][self.room_type]
        else:
            texture = self.all_textures["rooms"][self.floor_type]
        texture = texture.subsurface((texture_x, texture_y, consts.GAME_WIDTH // 2, consts.GAME_HEIGHT // 2))

        background = pg.Surface((consts.GAME_WIDTH, consts.GAME_HEIGHT))
        background.blits(
            (
                (texture, (0, 0)),
                (pg.transform.flip(texture, True, False), (consts.GAME_WIDTH // 2, 0)),
                (pg.transform.flip(texture, False, True), (0, consts.GAME_HEIGHT // 2)),
                (pg.transform.flip(texture, True, True), (consts.GAME_WIDTH // 2, consts.GAME_HEIGHT // 2))
            )
        )
        if self.room_type == consts.RoomsTypes.SPAWN:
            background.blit(self.all_textures["room"]["controls"], (0, 0))  # Показ управления в спавн команте (сделать)
        self.background = background

    def setup_entities(self, xml: XMLTree):
        """
        Загрузка комнаты из json/xml, пока не выбрали.
        Сейчас - заглушка.
        """
        for i in range(consts.ROOM_HEIGHT):
            for j in range(consts.ROOM_WIDTH):
                if random.random() > 0.5:
                    Rock((j, i), self.floor_type,
                         self.all_sounds["rock_crumble"], self.all_textures["rocks"],
                         self.rocks, self.colliadble_group, self.all_obstacles)  # .destroy()

        # Сделать класс дверей
        # Сделать класс врага, который ходить по земле и обходит препятствия

    def update_obstacles(self):
        """
        Обновление списка препятствий. (нужно ли?)
        """
        pass

    def setup_graph(self):
        """
        Построение графа соседних клеток в комнате для передвижения противников.
        """
        cells = [[consts.RoomsTypes.DEFAULT] * consts.ROOM_WIDTH for _ in range(consts.ROOM_HEIGHT)]
        for obj in self.colliadble_group.sprites():
            cells[obj.y][obj.x] = consts.RoomsTypes.EMPTY  # noqa
        self.paths = make_neighbors_graph(cells)
        self.fly_paths = make_neighbors_graph(cells, use_diagonals=True)

    def add_door(self, xy_pos: tuple[int, int], door_type: consts.RoomsTypes | consts.FloorsTypes, is_open: bool):
        """
        Добавление дверей.
        """
        pass
    
    def add_other(self, xy_pos: tuple[int, int], *args):
        pass
    
    def exit_animtaion(self, direction: consts.Moves):
        self.moving = True

    def enter_animation(self, direction: consts.Moves):
        self.moving = True

    def render(self, screen: pg.Surface):
        if not self.moving:
            screen.blit(self.background, (0, consts.STATS_HEIGHT))
            self.all_obstacles.draw(screen)
        else:
            # Анимация перехода
            self.moving = False
