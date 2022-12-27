import random

import pygame as pg

import xml.etree.ElementTree as XMLTree

from src import consts
from src.utils.funcs import load_image, load_sound
from src.modules.entities.Rock import Rock
from src.modules.entities.Poop import Poop
from src.modules.entities.Door import Door
from src.utils.graph import make_neighbors_graph


class Room:
    controls_hint: pg.Surface = load_image("textures/room/controls.png")
    basement_background: pg.Surface = load_image("textures/room/basement.png")
    caves_background: pg.Surface = load_image("textures/room/caves.png")
    catacombs_background: pg.Surface = load_image("textures/room/basement.png")
    depths_background: pg.Surface = load_image("textures/room/basement.png")
    bluewomb_background: pg.Surface = load_image("textures/room/basement.png")
    womb_background: pg.Surface = load_image("textures/room/basement.png")

    treasure_background: pg.Surface = load_image("textures/room/basement.png")
    shop_background: list[pg.Surface] = [load_image("textures/room/shop.png"), load_image("textures/room/shop2.png")]
    secret_background: pg.Surface = load_image("textures/room/basement.png")

    """
    Класс комнаты.

    :param floor_type: Номер этажа (1-5).
    :param room_type: Тип комнаты.
    :param texture_variant: Вариант текстуры (1-4, один из вариантов из изображения).
    :param abs_pos: Расположение на всей карте (x, y).
    :param xml_description: XML разметка объектов в комнате.
    """

    def __init__(self, floor_type: consts.FloorsTypes | str,
                 room_type: consts.RoomsTypes | str,
                 texture_variant: int,
                 abs_pos: tuple[int, int],
                 xml_description: XMLTree):

        self.x, self.y = abs_pos
        self.floor_type = floor_type
        self.room_type = room_type
        self.texture_variant = texture_variant
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
        self.setup_graph()

    def setup_background(self):
        texture_x = texture_y = 0
        if self.texture_variant == 2:
            texture_x = consts.GAME_WIDTH // 2
        elif self.texture_variant == 3:
            texture_y = consts.GAME_HEIGHT // 2
        elif self.texture_variant == 4:
            texture_x = consts.GAME_WIDTH // 2
            texture_y = consts.GAME_HEIGHT // 2

        if self.room_type in (consts.RoomsTypes.TREASURE, consts.RoomsTypes.SHOP, consts.RoomsTypes.SECRET):
            texture = getattr(Room, self.room_type.value.lower() + '_background')
        else:
            texture = getattr(Room, self.floor_type.value.lower() + '_background')
        if isinstance(texture, list):
            texture = random.choice(texture)
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
            # Показ управления в спавн команте
            background.blit(Room.controls_hint, (consts.WALL_SIZE, consts.WALL_SIZE))
        self.background = background

    def setup_entities(self, xml: XMLTree):
        """
        Загрузка комнаты из json/xml, пока не выбрали.
        Сейчас - заглушка.
        """
        for i in range(consts.ROOM_HEIGHT):
            for j in range(consts.ROOM_WIDTH):
                chance = random.random()
                if chance > 0.75:
                    Rock((j, i), self.floor_type, self.room_type, self.rocks, self.colliadble_group, self.all_obstacles)
                elif chance > 0.25:
                    Poop((j, i), self.poops, self.colliadble_group, self.destroyable_group, self.all_obstacles)

        for coords in consts.DoorsCoords:
            if random.random() > 0.5:
                door = Door(coords, self.floor_type, self.room_type, self.doors, self.all_obstacles)
                # door.blow()

        # Сделать логику для установки нужных дверей в нужные комнаты (класс этажа)
        # Сделать класс врага, который ходить по земле и обходит препятствия

    def setup_graph(self):
        """
        Построение графа соседних клеток в комнате для передвижения противников.
        """
        cells = [[consts.RoomsTypes.DEFAULT] * consts.ROOM_WIDTH for _ in range(consts.ROOM_HEIGHT)]
        for obj in self.colliadble_group.sprites():
            cells[obj.y][obj.x] = consts.RoomsTypes.EMPTY  # noqa
        self.paths = make_neighbors_graph(cells)
        self.fly_paths = make_neighbors_graph(cells, use_diagonals=True)

    def update_doors(self, xy_pos: tuple[int, int], is_open: bool):
        """
        Хз зачем
        """
        pass

    def add_other(self, xy_pos: tuple[int, int], *args):
        pass

    def exit_animtaion(self, direction: consts.Moves):
        self.moving = True

    def enter_animation(self, direction: consts.Moves):
        self.moving = True

    def update(self, delta_t: float):
        """
        Обновление комнаты (перемещение врагов, просчёт коллизий)
        """
        pass

    def render(self, screen: pg.Surface):
        if not self.moving:
            screen.blit(self.background, (0, consts.STATS_HEIGHT))
            self.all_obstacles.draw(screen)
        else:
            # Анимация перехода
            self.moving = False
