import pygame as pg

from src.consts import CELL_SIZE, DoorsCoords, RoomsTypes, FloorsTypes
from src.utils.funcs import load_image, load_sound
from src.modules.entities.BaseItem import BaseItem


DOOR_CELL_SIZE = CELL_SIZE * 1.5


class Door(BaseItem):
    doors = load_image("textures/room/doors.png")

    basement_open_up = doors.subsurface(0, 0, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    basement_open_down = pg.transform.rotate(basement_open_up, 180)
    basement_open_left = pg.transform.rotate(basement_open_up, 90)
    basement_open_right = pg.transform.rotate(basement_open_up, 270)
    basement_close_up = doors.subsurface(0, DOOR_CELL_SIZE, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    basement_close_down = pg.transform.rotate(basement_close_up, 180)
    basement_close_left = pg.transform.rotate(basement_close_up, 90)
    basement_close_right = pg.transform.rotate(basement_close_up, 270)
    basement_blow_up = doors.subsurface(0, DOOR_CELL_SIZE * 2, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    basement_blow_down = pg.transform.rotate(basement_blow_up, 180)
    basement_blow_left = pg.transform.rotate(basement_blow_up, 90)
    basement_blow_right = pg.transform.rotate(basement_blow_up, 270)

    caves_open_up = doors.subsurface(DOOR_CELL_SIZE, 0, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    caves_open_down = pg.transform.rotate(caves_open_up, 180)
    caves_open_left = pg.transform.rotate(caves_open_up, 90)
    caves_open_right = pg.transform.rotate(caves_open_up, 270)
    caves_close_up = doors.subsurface(DOOR_CELL_SIZE, DOOR_CELL_SIZE, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    caves_close_down = pg.transform.rotate(caves_open_up, 180)
    caves_close_left = pg.transform.rotate(caves_open_up, 90)
    caves_close_right = pg.transform.rotate(caves_open_up, 270)
    caves_blow_up = doors.subsurface(DOOR_CELL_SIZE, DOOR_CELL_SIZE * 2, DOOR_CELL_SIZE, DOOR_CELL_SIZE)
    caves_blow_down = pg.transform.rotate(caves_open_up, 180)
    caves_blow_left = pg.transform.rotate(caves_open_up, 90)
    caves_blow_right = pg.transform.rotate(caves_open_up, 270)

    def __init__(self, xy_pos: DoorsCoords | tuple[int, int],
                 floor_type: FloorsTypes,
                 room_type: RoomsTypes,
                 *groups: pg.sprite.AbstractGroup,
                 is_open: bool = False,
                 collidable: bool = True,
                 hurtable: bool = False):
        if isinstance(xy_pos, DoorsCoords):
            self.xy_pos = xy_pos.value
        else:
            self.xy_pos = xy_pos
        self.floor_type = floor_type
        self.room_type = room_type
        self.is_open = is_open
        self.state = ''
        self.texture = ''
        self.direction = ''

        super().__init__(self.xy_pos, *groups, collidable=collidable, hurtable=hurtable)
        self.set_image()
        self.set_rect()

    def blow(self):
        """
        Уничтожение/Взрыв двери.
        """
        self.update_texture('_blow_')

    def open(self):
        """
        Открыть дверь.
        """
        self.update_texture('_open_')

    def update_texture(self, texture: str):
        self.texture = texture
        self.is_open = True
        self.collidable = False
        self.image = getattr(Door, self.texture + self.state + self.direction)

    def set_image(self):
        if self.room_type in (RoomsTypes.SHOP, RoomsTypes.TREASURE, RoomsTypes.BOSS, RoomsTypes.SECRET):
            texture = self.room_type.value
        else:
            texture = self.floor_type.value

        if self.is_open:
            state = '_open_'
        else:
            state = '_close_'

        if self.xy_pos == DoorsCoords.UP.value:
            self.image = getattr(Door, texture + state + 'up')
            self.direction = 'up'
        elif self.xy_pos == DoorsCoords.DOWN.value:
            self.image = getattr(Door, texture + state + 'down')
            self.direction = 'down'
        elif self.xy_pos == DoorsCoords.LEFT.value:
            self.image = getattr(Door, texture + state + 'left')
            self.direction = 'left'
        elif self.xy_pos == DoorsCoords.RIGHT.value:
            self.image = getattr(Door, texture + state + 'right')
            self.direction = 'right'

        self.state = state
        self.texture = texture

    def collide(self, other):
        if self.collidable:
            pass
        if self.hurtable:
            pass
