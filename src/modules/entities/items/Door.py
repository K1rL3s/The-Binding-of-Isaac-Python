import pygame as pg

from src import consts
from src.consts import USE_KEY
from src.modules.BaseClasses import BaseItem, MoveSprite
from src.utils.funcs import load_image, crop
from src.modules.characters.parents import Player

DOOR_CELL_SIZE = int(consts.CELL_SIZE * 1.75)  # Размер клетки (ширины) двери.


# class DoorImage:
#     """
#     Изображение со всеми дверьми.
#     Почему-то при определении в DoorTextures выдаёт NameError, поэтому вынес в отдельный класс.
#     """
#     image = load_image("textures/room/doors.png")


class DoorTextures:  # class DoorTextures(DoorImage):
    """
    Текстурки дверей по отдельности.
    """
    all_doors = [
        [
            crop(load_image("textures/room/doors.png").subsurface(DOOR_CELL_SIZE * x,
                                                                  DOOR_CELL_SIZE * y,
                                                                  DOOR_CELL_SIZE,
                                                                  DOOR_CELL_SIZE))
            for y in range(4)
        ]
        for x in range(10)
    ]

    basement = all_doors[0]

    basement_close_up = basement[0]
    basement_close_left = pg.transform.rotate(basement_close_up, 90)
    basement_close_down = pg.transform.rotate(basement_close_up, 180)
    basement_close_right = pg.transform.rotate(basement_close_up, 270)
    basement_open_up = basement[1]
    basement_open_left = pg.transform.rotate(basement_open_up, 90)
    basement_open_down = pg.transform.rotate(basement_open_up, 180)
    basement_open_right = pg.transform.rotate(basement_open_up, 270)
    basement_blow_up = basement[2]
    basement_blow_left = pg.transform.rotate(basement_blow_up, 90)
    basement_blow_down = pg.transform.rotate(basement_blow_up, 180)
    basement_blow_right = pg.transform.rotate(basement_blow_up, 270)
    basement_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    basement_secret_close_down = basement_secret_close_up
    basement_secret_close_left = basement_secret_close_up
    basement_secret_close_right = basement_secret_close_up
    basement_secret_blow_up = basement[3]
    basement_secret_blow_left = pg.transform.rotate(basement_secret_blow_up, 90)
    basement_secret_blow_down = pg.transform.rotate(basement_secret_blow_up, 180)
    basement_secret_blow_right = pg.transform.rotate(basement_secret_blow_up, 270)

    caves = all_doors[1]
    caves_close_up = caves[0]
    caves_close_left = pg.transform.rotate(caves_close_up, 90)
    caves_close_down = pg.transform.rotate(caves_close_up, 180)
    caves_close_right = pg.transform.rotate(caves_close_up, 270)
    caves_open_up = caves[1]
    caves_open_left = pg.transform.rotate(caves_open_up, 90)
    caves_open_down = pg.transform.rotate(caves_open_up, 180)
    caves_open_right = pg.transform.rotate(caves_open_up, 270)
    caves_blow_up = caves[2]
    caves_blow_left = pg.transform.rotate(caves_blow_up, 90)
    caves_blow_down = pg.transform.rotate(caves_blow_up, 180)
    caves_blow_right = pg.transform.rotate(caves_blow_up, 270)
    caves_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    caves_secret_close_down = caves_secret_close_up
    caves_secret_close_left = caves_secret_close_up
    caves_secret_close_right = caves_secret_close_up
    caves_secret_blow_up = caves[3]
    caves_secret_blow_left = pg.transform.rotate(caves_secret_blow_up, 90)
    caves_secret_blow_down = pg.transform.rotate(caves_secret_blow_up, 180)
    caves_secret_blow_right = pg.transform.rotate(caves_secret_blow_up, 270)

    catacombs = all_doors[2]
    catacombs_close_up = catacombs[0]
    catacombs_close_left = pg.transform.rotate(catacombs_close_up, 90)
    catacombs_close_down = pg.transform.rotate(catacombs_close_up, 180)
    catacombs_close_right = pg.transform.rotate(catacombs_close_up, 270)
    catacombs_open_up = catacombs[1]
    catacombs_open_left = pg.transform.rotate(catacombs_open_up, 90)
    catacombs_open_down = pg.transform.rotate(catacombs_open_up, 180)
    catacombs_open_right = pg.transform.rotate(catacombs_open_up, 270)
    catacombs_blow_up = catacombs[2]
    catacombs_blow_left = pg.transform.rotate(catacombs_blow_up, 90)
    catacombs_blow_down = pg.transform.rotate(catacombs_blow_up, 180)
    catacombs_blow_right = pg.transform.rotate(catacombs_blow_up, 270)
    catacombs_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    catacombs_secret_close_down = catacombs_secret_close_up
    catacombs_secret_close_left = catacombs_secret_close_up
    catacombs_secret_close_right = catacombs_secret_close_up
    catacombs_secret_blow_up = catacombs[3]
    catacombs_secret_blow_left = pg.transform.rotate(catacombs_secret_blow_up, 90)
    catacombs_secret_blow_down = pg.transform.rotate(catacombs_secret_blow_up, 180)
    catacombs_secret_blow_right = pg.transform.rotate(catacombs_secret_blow_up, 270)

    depths = all_doors[3]
    depths_close_up = depths[0]
    depths_close_left = pg.transform.rotate(depths_close_up, 90)
    depths_close_down = pg.transform.rotate(depths_close_up, 180)
    depths_close_right = pg.transform.rotate(depths_close_up, 270)
    depths_open_up = depths[1]
    depths_open_left = pg.transform.rotate(depths_open_up, 90)
    depths_open_down = pg.transform.rotate(depths_open_up, 180)
    depths_open_right = pg.transform.rotate(depths_open_up, 270)
    depths_blow_up = depths[2]
    depths_blow_left = pg.transform.rotate(depths_blow_up, 90)
    depths_blow_down = pg.transform.rotate(depths_blow_up, 180)
    depths_blow_right = pg.transform.rotate(depths_blow_up, 270)
    depths_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    depths_secret_close_down = depths_secret_close_up
    depths_secret_close_left = depths_secret_close_up
    depths_secret_close_right = depths_secret_close_up
    depths_secret_blow_up = depths[3]
    depths_secret_blow_left = pg.transform.rotate(depths_secret_blow_up, 90)
    depths_secret_blow_down = pg.transform.rotate(depths_secret_blow_up, 180)
    depths_secret_blow_right = pg.transform.rotate(depths_secret_blow_up, 270)

    bluewomb = all_doors[4]
    bluewomb_close_up = bluewomb[0]
    bluewomb_close_left = pg.transform.rotate(bluewomb_close_up, 90)
    bluewomb_close_down = pg.transform.rotate(bluewomb_close_up, 180)
    bluewomb_close_right = pg.transform.rotate(bluewomb_close_up, 270)
    bluewomb_open_up = bluewomb[1]
    bluewomb_open_left = pg.transform.rotate(bluewomb_open_up, 90)
    bluewomb_open_down = pg.transform.rotate(bluewomb_open_up, 180)
    bluewomb_open_right = pg.transform.rotate(bluewomb_open_up, 270)
    bluewomb_blow_up = bluewomb[2]
    bluewomb_blow_left = pg.transform.rotate(bluewomb_blow_up, 90)
    bluewomb_blow_down = pg.transform.rotate(bluewomb_blow_up, 180)
    bluewomb_blow_right = pg.transform.rotate(bluewomb_blow_up, 270)
    bluewomb_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    bluewomb_secret_close_down = bluewomb_secret_close_up
    bluewomb_secret_close_left = bluewomb_secret_close_up
    bluewomb_secret_close_right = bluewomb_secret_close_up
    bluewomb_secret_blow_up = bluewomb[3]
    bluewomb_secret_blow_left = pg.transform.rotate(bluewomb_secret_blow_up, 90)
    bluewomb_secret_blow_down = pg.transform.rotate(bluewomb_secret_blow_up, 180)
    bluewomb_secret_blow_right = pg.transform.rotate(bluewomb_secret_blow_up, 270)

    womb = all_doors[5]
    womb_close_up = womb[0]
    womb_close_left = pg.transform.rotate(womb_close_up, 90)
    womb_close_down = pg.transform.rotate(womb_close_up, 180)
    womb_close_right = pg.transform.rotate(womb_close_up, 270)
    womb_open_up = womb[1]
    womb_open_left = pg.transform.rotate(womb_open_up, 90)
    womb_open_down = pg.transform.rotate(womb_open_up, 180)
    womb_open_right = pg.transform.rotate(womb_open_up, 270)
    womb_blow_up = womb[2]
    womb_blow_left = pg.transform.rotate(womb_blow_up, 90)
    womb_blow_down = pg.transform.rotate(womb_blow_up, 180)
    womb_blow_right = pg.transform.rotate(womb_blow_up, 270)
    womb_secret_close_up = pg.Surface((DOOR_CELL_SIZE, DOOR_CELL_SIZE))
    womb_secret_close_down = bluewomb_secret_close_up
    womb_secret_close_left = bluewomb_secret_close_up
    womb_secret_close_right = bluewomb_secret_close_up
    womb_secret_blow_up = womb[3]
    womb_secret_blow_left = pg.transform.rotate(womb_secret_blow_up, 90)
    womb_secret_blow_down = pg.transform.rotate(womb_secret_blow_up, 180)
    womb_secret_blow_right = pg.transform.rotate(womb_secret_blow_up, 270)

    boss = all_doors[6]
    boss_close_up = boss[0]
    boss_close_left = pg.transform.rotate(boss_close_up, 90)
    boss_close_down = pg.transform.rotate(boss_close_up, 180)
    boss_close_right = pg.transform.rotate(boss_close_up, 270)
    boss_open_up = boss[1]
    boss_open_down = pg.transform.rotate(boss_open_up, 180)
    boss_open_left = pg.transform.rotate(boss_open_up, 90)
    boss_open_right = pg.transform.rotate(boss_open_up, 270)

    treasure = all_doors[7]
    treasure_close_up = treasure[0]
    treasure_close_left = pg.transform.rotate(treasure_close_up, 90)
    treasure_close_down = pg.transform.rotate(treasure_close_up, 180)
    treasure_close_right = pg.transform.rotate(treasure_close_up, 270)
    treasure_open_up = treasure[1]
    treasure_open_down = pg.transform.rotate(treasure_open_up, 180)
    treasure_open_left = pg.transform.rotate(treasure_open_up, 90)
    treasure_open_right = pg.transform.rotate(treasure_open_up, 270)

    shop = all_doors[8]
    shop_close_up = shop[0]
    shop_close_left = pg.transform.rotate(shop_close_up, 90)
    shop_close_down = pg.transform.rotate(shop_close_up, 180)
    shop_close_right = pg.transform.rotate(shop_close_up, 270)
    shop_open_up = shop[1]
    shop_open_left = pg.transform.rotate(shop_open_up, 90)
    shop_open_down = pg.transform.rotate(shop_open_up, 180)
    shop_open_right = pg.transform.rotate(shop_open_up, 270)


class Door(BaseItem, DoorTextures):
    """
    Класс двери.

    :param floor_type: Тип этажа.
    :param room_type: Тип комнаты (текстурки).
    :param groups: Группы спрайтов.
    :param collidable: Закрыта ли дверь.
    :param hurtable: Наносит ли урон дверь при проходе через неё.
    """
    def __init__(self,
                 xy_pos: consts.DoorsCoords | tuple[int, int],
                 floor_type: consts.FloorsTypes,
                 from_room_type: consts.RoomsTypes,
                 to_room_type: consts.RoomsTypes,  # из этого определять текстурку (секретка в т.ч.)
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = True,
                 hurtable: bool = False):
        if isinstance(xy_pos, consts.DoorsCoords):
            self.xy_pos = xy_pos.value
        else:
            self.xy_pos = xy_pos
        self.floor_type = floor_type
        self.to_room_type = to_room_type
        self.from_room_type = from_room_type
        self.state = ''
        self.texture = ''
        self.direction = ''
        self.room_finished = False

        BaseItem.__init__(self, self.xy_pos, *groups, collidable=collidable, hurtable=hurtable)
        self.set_image()
        BaseItem.set_rect(self)
        self.set_rect()
        self.event_rect = pg.Rect(0, 0, 50, 50)
        self.event_rect.center = self.rect.center

    def set_rect(self, width: int | None = None, height: int | None = None, up: int = 0, left: int = 0):
        if self.to_room_type == consts.RoomsTypes.SECRET:
            image: pg.Surface = getattr(DoorTextures, f'{self.floor_type.value}_blow_{self.direction}')
            self.rect = image.get_rect()
        if self.direction == 'up':
            self.rect.midbottom = (consts.WIDTH // 2, consts.WALL_SIZE)
        elif self.direction == 'down':
            self.rect.midtop = (consts.WIDTH // 2, consts.GAME_HEIGHT - consts.WALL_SIZE)
        elif self.direction == 'left':
            self.rect.midright = (consts.WALL_SIZE,
                                  consts.WALL_SIZE + consts.CELL_SIZE * consts.ROOM_HEIGHT // 2)
        elif self.direction == 'right':
            self.rect.midleft = (consts.WIDTH - consts.WALL_SIZE,
                                 consts.WALL_SIZE + consts.CELL_SIZE * consts.ROOM_HEIGHT // 2)

    def blow(self, with_sound: bool = True):
        """
        Уничтожение/Взрыв двери.

        :param with_sound: Со звуком ли.
        """
        if not self.collidable:
            return
        if self.to_room_type in (consts.RoomsTypes.BOSS, consts.RoomsTypes.TREASURE, consts.RoomsTypes.SHOP):
            return
        self.update_image('blow', with_sound=with_sound)

    def open(self, with_sound: bool = True, with_key: bool = False):
        """
        Открыть дверь.

        :param with_sound: Со звуком ли.
        :param with_key: Открывается ли ключом.
        """
        with_key = with_key or self.from_room_type in (consts.RoomsTypes.SHOP, consts.RoomsTypes.TREASURE)
        self.room_finished = True
        if not self.collidable:
            return
        if self.to_room_type == consts.RoomsTypes.SECRET:
            return
        if self.to_room_type in (consts.RoomsTypes.SHOP, consts.RoomsTypes.TREASURE) and not with_key:
            return
        self.update_image("open", with_sound=with_sound)

    def close(self, with_sound: bool = True):
        """
        Закрыть двери.

        :param with_sound: Со звуком ли.
        """
        self.update_image('close', with_sound=with_sound)

    def update_image(self, state: str = None, direction: str = None, with_sound: bool = True):
        """
        Обновление текстурки двери.

        :param state: Открыта, закрыта или взорвана.
        :param direction: Сверху, снизу, слева или справа.
        :param with_sound: Со звуком ли.
        """
        if state:
            self.state = state
        if direction:
            self.direction = direction
        self.collidable = self.state == 'close'

        if self.to_room_type == consts.RoomsTypes.SECRET and self.collidable:
            self.image = pg.Surface((0, 0))
        else:
            self.image = getattr(Door, f'{self.texture}_{self.state}_{self.direction}')

        if with_sound:
            self.play_sound()

    def play_sound(self):
        """
        Проигрыш звука открытия/закрытия.
        """
        pass

    def set_image(self):
        """
        Определяет state, direction и texture при инициализации для метода update_image.
        """
        if self.to_room_type in (consts.RoomsTypes.SHOP, consts.RoomsTypes.TREASURE, consts.RoomsTypes.BOSS):
            self.texture = self.to_room_type.value
        elif self.to_room_type == consts.RoomsTypes.SECRET:
            self.texture = f'{self.floor_type.value}_{self.to_room_type.value}'
        else:
            self.texture = self.floor_type.value

        if self.collidable:
            self.state = 'close'
        else:
            self.state = 'open'

        if self.xy_pos == consts.DoorsCoords.UP.value:
            self.direction = 'up'
        elif self.xy_pos == consts.DoorsCoords.DOWN.value:
            self.direction = 'down'
        elif self.xy_pos == consts.DoorsCoords.LEFT.value:
            self.direction = 'left'
        elif self.xy_pos == consts.DoorsCoords.RIGHT.value:
            self.direction = 'right'

        self.update_image(self.state, self.direction)

    def collide(self, other: MoveSprite):
        if not BaseItem.collide(self, other):
            return

        if not self.room_finished:
            return

        if self.to_room_type in (consts.RoomsTypes.SHOP, consts.RoomsTypes.TREASURE) and isinstance(other, Player):
            if self.collidable and other.count_key:
                other.count_key -= 1
                self.open(with_key=True)
                pg.event.post(pg.event.Event(USE_KEY))

        # Вместо MovingEnemy поставить MainCharacter или его туловище
        if isinstance(other, Player) and self.event_rect.colliderect(other.rect):
            direction, next_coords = None, None
            if self.xy_pos == consts.DoorsCoords.UP.value:
                direction = consts.Moves.UP
                next_coords = consts.DoorsCoords.DOWN.value
                next_coords = next_coords[0], next_coords[1] - 1
            elif self.xy_pos == consts.DoorsCoords.DOWN.value:
                direction = consts.Moves.DOWN
                next_coords = consts.DoorsCoords.UP.value
                next_coords = next_coords[0], next_coords[1] + 1
            elif self.xy_pos == consts.DoorsCoords.RIGHT.value:
                direction = consts.Moves.RIGHT
                next_coords = consts.DoorsCoords.LEFT.value
                next_coords = next_coords[0] + 1, next_coords[1]
            elif self.xy_pos == consts.DoorsCoords.LEFT.value:
                direction = consts.Moves.LEFT
                next_coords = consts.DoorsCoords.RIGHT.value
                next_coords = next_coords[0] - 1, next_coords[1]
            assert direction
            pg.event.post(pg.event.Event(consts.MOVE_TO_NEXT_ROOM,
                                         {'direction': direction, 'next_coords': next_coords}))

            # Реализовать закрытие двери после входа в секретку:
            # if self.to_room_type == consts.RoomsTypes.SECRET:
            #     self.update_image("close")
