import pygame as pg

from src.modules.levels.LevelGenerator import generate_level
from src.modules.levels.Room import Room
from src.utils.graph import get_neighbors_coords
from src.consts import RoomsTypes, FloorsTypes, DoorsCoords, Moves


class Level:
    def __init__(self,
                 floor_type: FloorsTypes | str,
                 width: int = 10,
                 height: int = 10):
        self.width = width
        self.height = height
        self.floor_type = floor_type
        self.level_map: list[list[RoomsTypes | str]] = []
        self.rooms: list[list[Room | None]] = [[None] * width for _ in range(height)]
        self.current_room: Room | None = None

        self.setup_level()

    def setup_level(self):
        self.level_map = generate_level(self.width, self.height, 10)
        for y, row in enumerate(self.level_map):
            for x, room_type in enumerate(row):
                if room_type == RoomsTypes.EMPTY:
                    continue
                room = Room(self.floor_type, room_type, (x, y), None)
                room.setup_doors(self.get_doors(x, y))
                if room_type == RoomsTypes.SPAWN:
                    self.current_room = room
                # room.update_doors('blow')
                # room.update_doors('open')
                # room.update_doors('close')
                self.rooms[y][x] = room
        assert self.current_room is not None and self.current_room.room_type == RoomsTypes.SPAWN
        self.change_rooms_state(self.current_room.x, self.current_room.y)

    def get_doors(self, cur_x: int, cur_y: int) -> list[tuple[DoorsCoords, RoomsTypes]]:
        coords = get_neighbors_coords(cur_x, cur_y, self.level_map)
        doors = []
        for room_x, room_y in coords:
            direction = None
            if room_x > cur_x:
                direction = DoorsCoords.RIGHT
            elif room_x < cur_x:
                direction = DoorsCoords.LEFT
            elif room_y > cur_y:
                direction = DoorsCoords.DOWN
            elif room_y < cur_y:
                direction = DoorsCoords.UP
            assert direction is not None, f'Не удалось получить расположение двери'

            if (self.level_map[cur_y][cur_x] in
                    (RoomsTypes.TREASURE, RoomsTypes.BOSS, RoomsTypes.SECRET, RoomsTypes.SHOP) and
                    self.level_map[room_y][room_x] != RoomsTypes.SECRET):
                doors.append((direction, self.level_map[cur_y][cur_x]))
            else:
                doors.append((direction, self.level_map[room_y][room_x]))

        return doors

    def get_rooms(self) -> list[list[Room | None]]:
        return self.rooms

    def change_rooms_state(self, cur_x: int, cur_y: int):
        # Перенести в комнату, пусть там она сама своё состояние определяет и возвращает Surface нужный для Stats
        self.rooms[cur_y][cur_x].visited = True
        coords = get_neighbors_coords(cur_x, cur_y, self.level_map)
        for x, y in coords:
            self.rooms[y][x].spotted = True

    def move_to_next_room(self, direction: Moves | tuple[int, int]):
        x, y = direction.value
        x = self.current_room.x + x
        y = self.current_room.y + y
        if self.rooms[y][x]:
            self.current_room = self.rooms[y][x]
            self.current_room.visited = True
            self.change_rooms_state(x, y)

    def update(self, delta_t: float, *args, **kwargs):
        self.current_room.update(delta_t)

    def render(self, screen: pg.Surface):
        self.current_room.render(screen)
