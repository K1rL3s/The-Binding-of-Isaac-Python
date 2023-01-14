import random
import math

import pygame as pg

import xml.etree.ElementTree as XMLTree

from src.modules.BaseClasses import BaseItem, BaseEnemy
from src.modules.entities.items import (FirePlace, PickBomb, PickKey, PickMoney,
                                        Rock, Poop, Door, Spikes, Web, BlowBomb)
from src.modules.levels.Border import Border
from src.modules.enemies import ExampleEnemy
from src.utils.funcs import pixels_to_cell, load_image
from src.utils.graph import make_neighbors_graph
from src import consts

from src.modules.characters.parents import Player


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

    minimap_icons: dict[consts.RoomsTypes, pg.Surface] = {
        room_type: surface
        for room_type, surface in zip(
            (consts.RoomsTypes.SHOP, consts.RoomsTypes.BOSS, consts.RoomsTypes.TREASURE, consts.RoomsTypes.SECRET),
            [load_image("textures/room/minimap_icons.png").subsurface((x * 32, 0, 32, 32)) for x in range(4)]
        )
    }


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
                 floor_type: consts.FloorsTypes,
                 room_type: consts.RoomsTypes,
                 xy_pos: tuple[int, int],
                 main_hero: Player,
                 xml_description: XMLTree,
                 texture_variant: int = None):

        assert room_type != consts.RoomsTypes.EMPTY, f"Тип комнаты не можеть быть {consts.RoomsTypes.EMPTY}."

        self.x, self.y = xy_pos
        self.floor_type = floor_type
        self.room_type = room_type
        self.texture_variant = texture_variant if texture_variant else random.randint(1, 4)
        self.minimap_cell: pg.Surface = pg.Surface((0, 0))
        self.background: pg.Surface = pg.Surface((0, 0))
        self.paths_update_ticks = 0
        self.is_over = False  # Пройдена ли комната
        self.is_friendly = True  # Комната содержит только шипы, троль-бомбы итп, т.е. двери открыти, но ловушки есть

        # Отображение на мини-карте разными цветами
        self.is_spotted = False
        self.is_visited = False
        self.is_active = False

        self.debug_render = pg.sprite.Group()  # Отрисовка того, что обычно не видно
        self.colliadble_group = pg.sprite.Group()  # То, через что нельзя пройти, пока оно есть
        self.obstacles = pg.sprite.Group()  # Препятствия для построения графа комнаты
        self.blowable = pg.sprite.Group()  # То, что взрывается
        self.main_hero_group = pg.sprite.Group()
        self.main_hero_group.add(main_hero.body)
        self.movement_borders = pg.sprite.Group()  # Барьеры, не дающие пройти через себя
        self.tears_borders = pg.sprite.Group()  # Барьеры, не дающие слезам пролететь через себя

        self.enemies = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.poops = pg.sprite.Group()
        self.webs = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.other = pg.sprite.Group()  # Бомбы, ключи, монеты итд итп
        self.paths = dict()  # Пути для наземных
        self.fly_paths = dict()  # Пути для летающих врагов

        self.main_hero = main_hero

        self.setup_background()
        self.setup_entities(xml_description)
        self.setup_graph()
        self.setup_borders()

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
        for i in range(consts.ROOM_HEIGHT):
            for j in range(consts.ROOM_WIDTH):
                chance = random.random()
                if chance > 0.9:
                    Rock((j, i), self.floor_type, self.room_type, self.colliadble_group, self.rocks,
                         self.obstacles, self.blowable)
                elif chance > 0.8:
                    Poop((j, i), self.colliadble_group, self.poops, self.obstacles, self.blowable)
                elif chance > 0.7:
                    ExampleEnemy((j, i), self.paths, self.main_hero,
                                 (self.colliadble_group, self.movement_borders, self.other),
                                 (self.colliadble_group, self.tears_borders, self.other, self.main_hero_group),
                                 self.enemies, self.blowable)
                    self.is_friendly = False
                elif chance > 0.6:
                    Web((j, i), self.colliadble_group, self.webs, self.blowable)
                elif chance > 0.5:
                    FirePlace((j, i), self.colliadble_group, self.fires, self.blowable,
                              fire_type=consts.FirePlacesTypes.DEFAULT,
                              tear_collide_groups=(self.colliadble_group, self.tears_borders, self.other, self.enemies),
                              main_hero=self.main_hero.body)  # Передавать как-то хитрее?
                elif chance > 0.49:
                    Spikes((j, i), self.colliadble_group, self.spikes, hiding_delay=1, hiding_time=1)

    def setup_graph(self):
        """
        Построение графа соседних клеток в комнате для передвижения противников.
        """
        cells = [[consts.RoomsTypes.DEFAULT] * consts.ROOM_WIDTH for _ in range(consts.ROOM_HEIGHT)]

        if not self.fly_paths:
            self.fly_paths = make_neighbors_graph(cells, use_diagonals=True)

        for obj in self.obstacles.sprites():
            obj: BaseItem
            if obj.collidable:
                cells[obj.y][obj.x] = consts.RoomsTypes.EMPTY
        self.paths = make_neighbors_graph(cells)

    def setup_doors(self, doors: list[tuple[consts.DoorsCoords, consts.RoomsTypes]]):
        """
        Установка дверей с нужными текстурками.
        """
        for coords, room_type in doors:
            Door(coords, self.floor_type, room_type, self.doors, self.colliadble_group, self.blowable)
        self.setup_door_borders(doors)

    def setup_door_borders(self, doors: list[tuple[consts.DoorsCoords, consts.RoomsTypes]]):
        """
        Установка барьеров стен, супер крутая функция.
        """
        doors = [door[0] for door in doors]
        all_coords = list(consts.DoorsCoords)
        for coords in doors:
            all_coords.remove(coords)

            if coords == consts.DoorsCoords.LEFT:
                Border(consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       1,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(consts.WALL_SIZE,
                       consts.WALL_SIZE + math.ceil(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       1,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.RIGHT:
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       1,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE + 4 * consts.CELL_SIZE,
                       1,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.UP:
                Border(consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.debug_render)
                Border(consts.WALL_SIZE + math.ceil(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.debug_render)

            elif coords == consts.DoorsCoords.DOWN:
                Border(consts.WALL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(consts.WALL_SIZE + math.ceil(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.tears_borders, self.debug_render)

        for coords in all_coords:
            if coords == consts.DoorsCoords.LEFT:
                Border(consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       1,
                       consts.ROOM_HEIGHT * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.RIGHT:
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       1,
                       consts.ROOM_HEIGHT * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.UP:
                Border(consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       consts.ROOM_WIDTH * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.debug_render)

            elif coords == consts.DoorsCoords.DOWN:
                Border(consts.WALL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       consts.ROOM_WIDTH * consts.CELL_SIZE,
                       1,
                       self.movement_borders, self.tears_borders, self.debug_render)

    def setup_borders(self):
        """
        Установка барьеров на краях экрана.
        """
        # Лево
        Border(0, 0, 1, consts.GAME_HEIGHT,
               self.movement_borders, self.tears_borders, self.debug_render, is_killing=True)
        # Верх
        Border(0, 0, consts.WIDTH, 1,
               self.movement_borders, self.tears_borders, self.debug_render, is_killing=True)
        # Низ
        Border(0, consts.GAME_HEIGHT - 1, consts.WIDTH, 1,
               self.movement_borders, self.tears_borders, self.debug_render, is_killing=True)
        # Право
        Border(consts.WIDTH - 1, 0, 1, consts.GAME_HEIGHT,
               self.movement_borders, self.tears_borders, self.debug_render, is_killing=True)

    def update_doors(self, state: str, with_sound: bool = True):
        """
        Открыть/Закрыть/Взорвать все двери.

        :param state: "open", "close", "blow".
        :param with_sound: Со звуком ли.
        """
        for door in self.doors.sprites():
            getattr(door, state)(with_sound=with_sound)

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
        # Если убрать .copy(), то будет забавный баг)
        if self.is_active:
            self.minimap_cell = self.minimap_cells[2].copy()
        elif self.is_visited:
            self.minimap_cell = self.minimap_cells[1].copy()
        elif self.is_spotted:
            self.minimap_cell = self.minimap_cells[0].copy()

        # Особое отображение секретки после посещения
        if self.room_type == consts.RoomsTypes.SECRET and self.is_visited and not self.is_active:
            self.minimap_cell = self.minimap_cells[0].copy()

    def get_minimap_cell(self) -> pg.Surface:
        """
        Возвращает иконку для миникарты.

        :return: pg.Surface.
        """
        if self.minimap_cell.get_width():
            self.draw_minimap_icons()
        return self.minimap_cell

    def draw_minimap_icons(self):
        if icon := RoomTextures.minimap_icons.get(self.room_type):
            self.minimap_cell.blit(icon, ((consts.MINIMAP_CELL_WIDTH - icon.get_width()) // 2,
                                          (consts.MINIMAP_CELL_HEIGHT - icon.get_height()) // 2))

    def add_other(self, xy_pos: tuple[int, int], *args):
        pass

    def update(self, delta_t: float):
        """
        Обновление комнаты (перемещение врагов, просчёт коллизий)
        """
        self.other.update(delta_t)
        self.spikes.update(delta_t)
        self.webs.update(delta_t)
        self.fires.update(delta_t)

        if self.is_over:
            return

        self.paths_update_ticks += delta_t
        if self.paths_update_ticks >= self.paths_update_delay:
            self.paths_update_ticks = 0
            self.setup_graph()
            self.update_enemies_paths()
        self.enemies.update(delta_t)

        if not self.enemies.sprites():
            self.win_room()

    def update_enemies_paths(self):
        """
        Обновление графа комнаты для врагов (после поломки Poop'a пригождается).
        """
        for enemy in self.enemies:
            enemy: BaseEnemy
            enemy.update_room_graph(self.paths)

    def win_room(self):
        """
        Открытие всех дверей итд, когда все враги умерли.
        """
        self.is_over = True
        self.update_doors("open")
        if not self.is_friendly:
            for spikes in self.spikes.sprites():
                spikes: Spikes
                spikes.hide(True)

    def get_room_groups(self) -> tuple[tuple[pg.sprite.Group, ...], tuple[pg.sprite.Group, ...]]:
        return (
            (self.colliadble_group, self.movement_borders, self.other, self.doors),
            (self.colliadble_group, self.tears_borders, self.other, self.enemies)
        )

    def render(self, screen: pg.Surface):
        screen.blit(self.background, (0, 0))
        self.doors.draw(screen)
        self.rocks.draw(screen)
        self.poops.draw(screen)
        self.webs.draw(screen)
        self.spikes.draw(screen)
        self.fires.draw(screen)
        self.other.draw(screen)
        self.enemies.draw(screen)

        for enemy in self.enemies.sprites():
            enemy: ExampleEnemy
            enemy.draw_tears(screen)
            # enemy.draw_stats(screen)  # СНИЖАЕТ ФПС!!!
        for fire in self.fires.sprites():
            fire: FirePlace
            fire.draw_tears(screen)
        # self.debug_render.draw(screen)

        self.main_hero.render(screen)

    def test_func_set_bomb(self, xy_pos: tuple[int, int]):
        xy_pos = (xy_pos[0], xy_pos[1] - consts.STATS_HEIGHT)
        if room_pos := pixels_to_cell(xy_pos):
            BlowBomb(room_pos, (self.colliadble_group, self.movement_borders, self.other),
                     (self.blowable, self.other, self.main_hero_group), self.other, xy_pixels=xy_pos)

    def test_func_set_pickable(self, xy_pos: tuple[int, int]):
        xy_pos = (xy_pos[0], xy_pos[1] - consts.STATS_HEIGHT)
        if room_pos := pixels_to_cell(xy_pos):
            chance = random.random()
            if chance > 0.66:
                PickMoney(room_pos, (self.colliadble_group, self.movement_borders, self.other), self.other,
                          xy_pixels=xy_pos)
            elif chance > 0.33:
                PickBomb(room_pos, (self.colliadble_group, self.movement_borders, self.other), self.other,
                         xy_pixels=xy_pos)
            else:
                PickKey(room_pos, (self.colliadble_group, self.movement_borders, self.other), self.other,
                        xy_pixels=xy_pos)
