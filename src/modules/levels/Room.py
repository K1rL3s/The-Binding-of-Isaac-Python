import random

import pygame as pg

import xml.etree.ElementTree as XMLTree

from src import consts
from src.utils.funcs import load_image
from src.modules.BaseClasses.BaseItem import BaseItem
from src.modules.BaseClasses.BaseEnemy import BaseEnemy
from src.modules.entities.items.Rock import Rock
from src.modules.entities.items.Poop import Poop
from src.modules.entities.items.Door import Door
from src.modules.enemies.ExampleEnemy import ExampleEnemy
from src.utils.graph import make_neighbors_graph


class RoomTextures:
    controls_hint: pg.Surface = load_image("textures/room/controls.png")
    basement_background: pg.Surface = load_image("textures/room/basement.png")
    caves_background: pg.Surface = load_image("textures/room/caves.png")
    catacombs_background: pg.Surface = load_image("textures/room/catacombs.png")
    depths_background: pg.Surface = load_image("textures/room/depths.png")
    bluewomb_background: pg.Surface = load_image("textures/room/bluewomb.png")
    womb_background: pg.Surface = load_image("textures/room/womb.png")

    treasure_background: pg.Surface = load_image("textures/room/treasure.png")
    shop_background: pg.Surface = load_image("textures/room/shop.png")
    secret_background: pg.Surface = load_image("textures/room/secret.png")

    minimap_cells: list[pg.Surface] = [load_image("textures/room/minimap_cells.png").subsurface(
            (0, y * consts.MINIMAP_CELL_HEIGHT, consts.MINIMAP_CELL_WIDTH, consts.MINIMAP_CELL_HEIGHT)
        )
        for y in range(3)
    ]


class Room(RoomTextures):
    """
    Класс комнаты.

    :param floor_type: Тип этажа.
    :param room_type: Тип комнаты.
    :param texture_variant: Вариант текстуры (1-4, один из вариантов из изображения).
    :param xy_pos: Расположение на этаже (x, y).
    :param main_hero: Главный герой.
    :param xml_description: XML разметка объектов в комнате.
    """
    paths_update_delay: int | float = 1

    def __init__(self,
                 floor_type: consts.FloorsTypes | str,
                 room_type: consts.RoomsTypes | str,
                 xy_pos: tuple[int, int],
                 main_hero,
                 xml_description: XMLTree,
                 texture_variant: int = None):

        assert room_type != consts.RoomsTypes.EMPTY, f"Тип комнаты не можеть быть {consts.RoomsTypes.EMPTY}."

        self.x, self.y = xy_pos
        self.floor_type = floor_type
        self.room_type = room_type
        self.texture_variant = texture_variant if texture_variant else random.randint(1, 4)
        self.minimap_cell: pg.Surface = pg.Surface((0, 0))
        self.background: pg.Surfac = pg.Surface((0, 0))
        self.paths_update_ticks = 0

        # Отображение на мини-карте разными цветами
        self.is_spotted = False
        self.is_visited = False
        self.is_active = False

        self.all_obstacles = pg.sprite.Group()
        self.colliadble_group = pg.sprite.Group()
        self.destroyable_group = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.fly_enemies = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.poops = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.other = pg.sprite.Group()  # Бомбы, ключи, монеты итд итп
        self.paths = dict()  # Пути для наземных
        self.fly_paths = dict()  # Пути для летающих врагов

        self.main_hero = main_hero
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
        if self.room_type == consts.RoomsTypes.SPAWN and self.floor_type == consts.FloorsTypes.BASEMENT:
            # Показ управления в спавн команте
            background.blit(Room.controls_hint, (consts.WALL_SIZE, consts.WALL_SIZE))
        self.background = background

    def setup_entities(self, xml: XMLTree):
        """
        Загрузка комнаты из json/xml, пока не выбрали.
        Сейчас - заглушка.
        """
        no_enemy = True
        for i in range(consts.ROOM_HEIGHT):
            for j in range(consts.ROOM_WIDTH):
                chance = random.random()
                if chance > 0.9:
                    Rock((j, i), self.floor_type, self.room_type, self.rocks, self.colliadble_group, self.all_obstacles)
                elif chance > 0:  # and no_enemy:
                    ExampleEnemy((j, i), self.paths, self.main_hero, (self.colliadble_group,), (self.colliadble_group,),
                                 self.enemies)
                    no_enemy = False
                # elif chance > 0.4:
                #     Poop((j, i), self.poops, self.colliadble_group, self.destroyable_group, self.all_obstacles)

    def setup_graph(self):
        """
        Построение графа соседних клеток в комнате для передвижения противников.
        """
        cells = [[consts.RoomsTypes.DEFAULT] * consts.ROOM_WIDTH for _ in range(consts.ROOM_HEIGHT)]

        if not self.fly_paths:
            self.fly_paths = make_neighbors_graph(cells, use_diagonals=True)

        for obj in self.colliadble_group.sprites():
            obj: BaseItem
            cells[obj.y][obj.x] = consts.RoomsTypes.EMPTY
        self.paths = make_neighbors_graph(cells)

    def setup_doors(self, doors: list[tuple[consts.DoorsCoords, consts.RoomsTypes]]):
        """
        Установка дверей с нужными текстурками.
        """
        for coords, room_type in doors:
            Door(coords, self.floor_type, room_type, self.doors, self.all_obstacles)

    def update_doors(self, state: str):
        """
        Открыть/Закрыть/Взорвать все двери.
        :param state: "open", "close", "blow".
        """
        for door in self.doors.sprites():
            try:
                getattr(door, state)()
            except AttributeError:
                pass

    def update_detection_state(self, is_spotted: bool = False, is_active: bool = False):
        """
        Обновление состояния видимости на миникарте.
        :param is_spotted: Замечена ли комната (дверь в неё).
        :param is_active: Текущая ли комната.
        """

        self.is_active = is_active
        if self.is_active:
            self.is_visited = True
        if (self.is_visited or is_spotted) and self.room_type != consts.RoomsTypes.SECRET:
            self.is_spotted = True
        self.update_minimap()

    def update_minimap(self):
        """
        Обновление иконки для мини-карты.
        """
        if self.is_active:
            self.minimap_cell = self.minimap_cells[2]
        elif self.is_visited:
            self.minimap_cell = self.minimap_cells[1]
        elif self.is_spotted:
            self.minimap_cell = self.minimap_cells[0]

    def get_minimap_cell(self) -> pg.Surface:
        """
        Возвращает иконку для миникарты.
        :return: pg.Surface.
        """
        return self.minimap_cell

    def add_other(self, xy_pos: tuple[int, int], *args):
        pass

    def update(self, delta_t: float):
        """
        Обновление комнаты (перемещение врагов, просчёт коллизий)
        """
        self.paths_update_ticks += delta_t
        if self.paths_update_ticks >= self.paths_update_delay:
            self.paths_update_ticks = 0
            self.setup_graph()
            self.update_enemies_paths()
        self.enemies.update(delta_t)
        self.fly_enemies.update(delta_t)

    def update_enemies_paths(self):
        """
        Обновление графа комнаты для врагов (после поломки Poop'a пригождается).
        """
        for enemy in self.enemies:
            enemy: BaseEnemy
            enemy.update_room_graph(self.paths)

    def render(self, screen: pg.Surface):
        screen.blit(self.background, (0, consts.STATS_HEIGHT))
        self.rocks.draw(screen)
        self.poops.draw(screen)
        self.enemies.draw(screen)
        self.fly_enemies.draw(screen)

        # ЗАТЫЧКА ГГ
        screen.blit(self.main_hero.image, (self.main_hero.rect.x, self.main_hero.rect.y))
        # ЗАТЫЧКА ГГ

        for enemy in self.enemies.sprites():
            enemy: ExampleEnemy
            enemy.draw_tears(screen)
            # enemy.draw_stats(screen)  # СНИЖАЕТ ФПС!!!
        # for fly_enemy in self.fly_enemies.sprites():
        #     fly_enemy: ExampleEnemy
        #     fly_enemy.draw_tears(screen)

        self.fires.draw(screen)
        self.doors.draw(screen)
        self.other.draw(screen)

