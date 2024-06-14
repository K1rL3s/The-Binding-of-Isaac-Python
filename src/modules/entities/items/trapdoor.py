import pygame as pg

from src.consts import CELL_SIZE, MOVE_TO_NEXT_LEVEL, ROOM_HEIGHT, ROOM_WIDTH
from src.modules.base_classes import BaseItem, MoveSprite
from src.modules.characters.main_hero import Player
from src.utils.funcs import crop, load_image, load_sound

DOOR_CELL_SIZE = int(CELL_SIZE * 1.75)  # Размер клетки (ширины) двери.


class Trapdoor(BaseItem):
    """
    Класс люка в полу. Его отец - комната босса.

    :param xy_pos: Позиция в комнате.
    :param groups: Все группы, которым принадлежит предмет-спрайт.
    :param collidable: Открыт ли люк.
    """

    trapdoor_close = crop(
        load_image("textures/room/doors.png").subsurface(
            9 * DOOR_CELL_SIZE,
            0,
            DOOR_CELL_SIZE,
            DOOR_CELL_SIZE,
        ),
    )
    trapdoor_open = crop(
        load_image("textures/room/doors.png").subsurface(
            9 * DOOR_CELL_SIZE,
            DOOR_CELL_SIZE,
            DOOR_CELL_SIZE,
            DOOR_CELL_SIZE,
        ),
    )
    open_sound = load_sound("sounds/boss_defeated.mp3")

    def __init__(self, *groups: pg.sprite.AbstractGroup, collidable: bool = False):
        BaseItem.__init__(
            self,
            (ROOM_WIDTH // 2, ROOM_HEIGHT // 2),
            *groups,
            collidable=collidable,
        )

        self.set_image()
        self.set_rect()

        if self.collidable:
            self.open()

    def set_image(self):
        self.image = Trapdoor.trapdoor_close

    def open(self, with_sound: bool = False):
        self.image = Trapdoor.trapdoor_open
        self.collidable = True
        if with_sound:
            Trapdoor.open_sound.play()

    def collide(self, other: MoveSprite):
        if not isinstance(other, Player):
            return

        if self.collidable:
            pg.event.post(pg.event.Event(MOVE_TO_NEXT_LEVEL))
