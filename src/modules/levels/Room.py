import random
import math

import pygame as pg

from src.modules.BaseClasses import BaseItem, BaseEnemy, ShootingEnemy
from src.modules.enemies.Envy import Envy
from src.modules.enemies.Pudge import Pudge
from src.modules.enemies.Teratoma import Teratoma
from src.modules.enemies.duke import Duke
from src.modules.enemies.fistula import Fistula
from src.modules.entities.items import (FirePlace, PickBomb, PickKey, PickMoney, Rock, Poop, ShopItem,
                                        Door, Spikes, Web, BlowBomb, Pedestal, PickHeart, Trapdoor)
from src.modules.entities.artifacts import (Dinner, FreshMeat, GreenSyringe, GreySyringe, MomsHeels,
                                            PurpleSyringe, RedSyringe, WhiteSyringe)
from src.modules.levels.Border import Border
from src.modules.enemies import Maw, Guts, Host
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
    """
    paths_update_delay: int | float = 1
    artifacts = [Dinner, FreshMeat, GreenSyringe, GreySyringe, MomsHeels, PurpleSyringe, RedSyringe, WhiteSyringe]
    loot = [PickHeart, PickKey, PickMoney, PickBomb]

    def __init__(self,
                 floor_type: consts.FloorsTypes,
                 room_type: consts.RoomsTypes,
                 xy_pos: tuple[int, int],
                 main_hero: Player,
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
        self.main_hero_group.add(main_hero)
        self.movement_borders = pg.sprite.Group()  # Барьеры, не дающие пройти через себя
        self.tears_borders = pg.sprite.Group()  # Барьеры, не дающие слезам пролететь через себя

        self.enemies = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.hp_bar_group = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.poops = pg.sprite.Group()
        self.webs = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.other = pg.sprite.Group()  # Бомбы, ключи, монеты итд итп
        self.artifacts_group = pg.sprite.Group()  # Артефакты
        self.paths = dict()  # Пути для наземных
        self.fly_paths = dict()  # Пути для летающих врагов

        self.main_hero = main_hero

        self.setup_background()
        self.setup_borders()
        self.setup_entities()
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

    def setup_entities(self):
        """
        Рандомная генерация вещей в комнате без какой-либо особой логики :)
        """
        centerx, centery = consts.ROOM_WIDTH // 2, consts.ROOM_HEIGHT // 2

        if self.room_type == consts.RoomsTypes.SPAWN:
            return

        if self.room_type == consts.RoomsTypes.BOSS and self.floor_type == consts.FloorsTypes.CATACOMBS:
            Teratoma((6, 3), 40, self.paths, self.main_hero,
                     (self.movement_borders, self.doors), self.hp_bar_group, 1, 2,
                     self.bosses, self.blowable)

        if self.room_type == consts.RoomsTypes.BOSS and self.floor_type == consts.FloorsTypes.BASEMENT:
            Fistula((6, 3), 40, self.paths, self.main_hero,
                    (self.movement_borders, self.doors), self.hp_bar_group, 1, 2,
                    self.bosses, self.blowable)

        if self.room_type == consts.RoomsTypes.BOSS and self.floor_type == consts.FloorsTypes.DEPTHS:
            Duke((6, 3), self.paths, self.main_hero,
                 (self.movement_borders, self.doors, self.main_hero_group),
                 (self.main_hero_group, self.colliadble_group), self.hp_bar_group,
                 1.4, self.bosses, self.blowable)

        if self.room_type == consts.RoomsTypes.BOSS and self.floor_type == consts.FloorsTypes.CAVES:
            Envy((6, 3), 40, self.paths, self.main_hero,
                 (self.movement_borders, self.doors), self.hp_bar_group, 1, 2,
                 self.bosses, self.blowable)

        if self.room_type == consts.RoomsTypes.BOSS and self.floor_type == consts.FloorsTypes.WOMB:
            Pudge((6, 3), 40, self.paths, self.main_hero,
                  (self.movement_borders, self.doors), self.hp_bar_group, 1, 2,
                  self.bosses, self.blowable)

        if self.room_type == consts.RoomsTypes.BOSS:
            self.is_friendly = False
            Trapdoor(self.colliadble_group, self.doors)
            return

        if self.room_type == consts.RoomsTypes.TREASURE:
            pedestal = Pedestal((centerx, centery),
                                self.obstacles, self.colliadble_group, self.other)
            pedestal.set_artifact(random.choice(Room.artifacts), self.artifacts_group)
            return

        if self.room_type == consts.RoomsTypes.SHOP:
            for i, items in zip(range(-2, 2 + 1, 2), (Room.artifacts, Room.loot, Room.loot)):
                ShopItem((centerx + i, centery), random.choice(items), self.other)
            return

        if self.room_type == consts.RoomsTypes.SECRET:
            for i in range(-2, 2 + 1, 2):
                self.set_pickable((centerx + i, centery))
            return

        enemies = 0
        max_enemies = 9
        max_pickable: int = 2
        max_host = max_guts = max_maw = max_spikes = 3
        count_pickable = count_host = count_guts = count_maw = count_spikes = 0
        for y in range(consts.ROOM_HEIGHT):
            for x in range(consts.ROOM_WIDTH):
                if y == centery or x == centerx:
                    continue
                chance = random.random()
                if chance > 0.9:
                    Rock((x, y), self.floor_type, self.room_type, self.colliadble_group, self.rocks,
                         self.obstacles, self.blowable)
                elif chance > 0.8:
                    Poop((x, y), self.colliadble_group, self.poops, self.obstacles, self.blowable)
                elif chance > 0.7:
                    Web((x, y), self.colliadble_group, self.webs, self.blowable)
                elif chance > 0.6:
                    fire_type = random.choices([consts.FirePlacesTypes.DEFAULT, consts.FirePlacesTypes.RED],
                                               [0.9, 0.1])[0]
                    FirePlace((x, y), self.colliadble_group, self.fires, self.blowable, self.obstacles,
                              fire_type=fire_type,
                              tear_collide_groups=(self.colliadble_group, self.tears_borders, self.main_hero_group),
                              main_hero=self.main_hero)
                elif chance > 0.5 and count_pickable < max_pickable:
                    self.set_pickable((x, y))
                    count_pickable += 1
                elif chance > 0.4 and enemies < max_enemies and count_maw < max_maw:
                    Maw((x, y), self.main_hero, (self.movement_borders, self.doors),
                        (self.colliadble_group, self.tears_borders, self.main_hero_group),
                        self.enemies, self.blowable)
                    enemies += 1
                    count_maw += 1
                elif chance > 0.35 and count_host < max_host:
                    Host((x, y), self.main_hero, (self.colliadble_group, self.movement_borders, self.doors),
                         (self.colliadble_group, self.tears_borders, self.main_hero_group),
                         self.enemies, self.blowable)
                    enemies += 1
                    count_host += 1
                elif chance > 0.3 and count_guts < max_guts:
                    Guts((x, y), self.paths, (self.colliadble_group, self.movement_borders, self.other),
                         self.enemies, self.blowable)
                    enemies += 1
                    count_guts += 1
                elif chance > 0.28 and count_spikes < max_spikes:
                    Spikes((x, y), self.colliadble_group, self.obstacles, self.spikes, hiding_delay=1, hiding_time=1)
                    count_spikes += 1

        self.is_friendly = not(bool(self.enemies) + bool(self.bosses))

    def setup_graph(self):
        """
        Построение графа соседних клеток в комнате для передвижения противников.
        """
        cells = [[consts.RoomsTypes.DEFAULT] * consts.ROOM_WIDTH for _ in range(consts.ROOM_HEIGHT)]

        if not self.fly_paths:
            self.fly_paths = make_neighbors_graph(cells, use_diagonals=True)

        for obj in self.obstacles.sprites():
            obj: BaseItem
            if obj.collidable or obj.hurtable:
                cells[obj.y][obj.x] = consts.RoomsTypes.EMPTY
        self.paths = make_neighbors_graph(cells)

    def setup_doors(self, doors: list[tuple[consts.DoorsCoords, consts.RoomsTypes]]):
        """
        Установка дверей с нужными текстурками.
        """
        for coords, to_room_type in doors:
            Door(coords, self.floor_type, self.room_type, to_room_type,
                 self.doors, self.colliadble_group, self.blowable)
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
                Border(0,
                       consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(0,
                       consts.WALL_SIZE + math.ceil(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.RIGHT:
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE + 4 * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       math.floor(consts.ROOM_HEIGHT / 2) * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.UP:
                Border(consts.WALL_SIZE,
                       0,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       self.movement_borders, self.debug_render)
                Border(consts.WALL_SIZE + math.ceil(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       0,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       self.movement_borders, self.debug_render)

            elif coords == consts.DoorsCoords.DOWN:
                Border(consts.WALL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)
                Border(consts.WALL_SIZE + math.ceil(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       math.floor(consts.ROOM_WIDTH / 2) * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

        for coords in all_coords:
            if coords == consts.DoorsCoords.LEFT:
                Border(0,
                       consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       consts.ROOM_HEIGHT * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.RIGHT:
                Border(consts.WIDTH - consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       consts.WALL_SIZE,
                       consts.ROOM_HEIGHT * consts.CELL_SIZE,
                       self.movement_borders, self.tears_borders, self.debug_render)

            elif coords == consts.DoorsCoords.UP:
                Border(consts.WALL_SIZE,
                       0,
                       consts.ROOM_WIDTH * consts.CELL_SIZE,
                       consts.WALL_SIZE,
                       self.movement_borders, self.debug_render)

            elif coords == consts.DoorsCoords.DOWN:
                Border(consts.WALL_SIZE,
                       consts.GAME_HEIGHT - consts.WALL_SIZE,
                       consts.ROOM_WIDTH * consts.CELL_SIZE,
                       consts.WALL_SIZE,
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

        if not self.enemies and not self.bosses:
            self.is_over = True
            self.win_room()

        self.paths_update_ticks += delta_t
        if self.paths_update_ticks >= self.paths_update_delay:
            self.paths_update_ticks = 0
            self.setup_graph()
            self.update_enemies_paths()
        self.enemies.update(delta_t)
        self.bosses.update(delta_t)

    def update_enemies_paths(self):
        """
        Обновление графа комнаты для врагов (после поломки Poop'a пригождается).
        """
        for enemy in self.enemies:
            enemy: BaseEnemy
            enemy.update_room_graph(self.paths)
        for boss in self.bosses:
            if isinstance(boss, BaseEnemy):
                boss.update_room_graph(self.paths)

    def win_room(self):
        """
        Открытие всех дверей итд, когда все враги умерли.
        """
        self.update_doors("open")
        if not self.is_friendly:
            for spikes in self.spikes.sprites():
                spikes: Spikes
                spikes.hide(True)

    def get_room_groups(self) -> tuple[tuple[pg.sprite.Group, ...], ...]:
        return (
            (self.movement_borders, self.doors, self.other, self.enemies, self.bosses),
            (self.colliadble_group, self.movement_borders, self.other, self.enemies, self.bosses),
            (self.colliadble_group, self.tears_borders, self.other, self.enemies, self.bosses)
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
        self.bosses.draw(screen)
        # self.movement_borders.draw(screen)
        self.artifacts_group.draw(screen)
        self.hp_bar_group.draw(screen)
        self.main_hero_group.draw(screen)

        for enemy in self.enemies.sprites():
            if isinstance(enemy, ShootingEnemy):
                enemy.draw_tears(screen)
        for fire in self.fires.sprites():
            if isinstance(fire, ShootingEnemy):
                fire.draw_tears(screen)

        # self.debug_render.draw(screen)

        self.main_hero.render(screen)

    def set_bomb(self, event: pg.event.Event):
        xy_pos = event.pos
        if room_pos := pixels_to_cell(xy_pos):
            BlowBomb(room_pos, (self.colliadble_group, self.movement_borders, self.other),
                     (self.blowable, self.other, self.main_hero_group), self.other, xy_pixels=xy_pos)

    def set_pickable(self, xy_pos: tuple[int, int]):  # Клетка
        chance = random.random()
        if chance > 0.75:
            PickMoney(xy_pos, (self.colliadble_group, self.movement_borders, self.other), self.other)
        elif chance > 0.50:
            PickBomb(xy_pos, (self.colliadble_group, self.movement_borders, self.other), self.other)
        elif chance > 0.25:
            PickHeart(xy_pos, (self.colliadble_group, self.movement_borders, self.other), self.other)
        elif chance < 0.20:
            PickKey(xy_pos, (self.colliadble_group, self.movement_borders, self.other), self.other)
