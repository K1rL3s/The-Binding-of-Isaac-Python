import pygame as pg

from src.consts import CELL_SIZE, DoorsCoords
from src.utils.funcs import load_image, load_sound
from src.modules.entities.BaseItem import BaseItem


class Door(BaseItem):
    doors: pg.Surface = load_image("textures/room/doors.png")
    basement_open_up: pg.Surface = doors.subsurface(0, 0, CELL_SIZE * 1.5, CELL_SIZE * 1.5)
    basement_open_down: pg.Surface = pg.transform.rotate(basement_open_up, 180)
    basement_open_left: pg.Surface = pg.transform.rotate(basement_open_up, 90)
    basement_open_right: pg.Surface = pg.transform.rotate(basement_open_up, 270)

    def __init__(self, xy_pos: DoorsCoords | tuple[int, int],
                 is_open: bool = False,
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = False,
                 hurtable: bool = False):
        if isinstance(xy_pos, DoorsCoords):
            self.xy_pos = xy_pos.value
        else:
            self.xy_pos = xy_pos
        self.is_open = is_open

        super().__init__(self.xy_pos, *groups, collidable=collidable, hurtable=hurtable)
        self.set_image()
        self.set_rect()

    def set_image(self):
        if self.xy_pos == DoorsCoords.UP.value:
            self.image = Door.basement_open_up
        elif self.xy_pos == DoorsCoords.DOWN.value:
            self.image = Door.basement_open_down
        elif self.xy_pos == DoorsCoords.LEFT.value:
            self.image = Door.basement_open_left
        elif self.xy_pos == DoorsCoords.RIGHT.value:
            self.image = Door.basement_open_right
