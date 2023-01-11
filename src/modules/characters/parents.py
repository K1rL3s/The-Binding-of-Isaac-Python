import pygame as pg

from typing import Type
from src.utils.funcs import load_image
from src.consts import CELL_SIZE
from src.consts import Moves
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear

LEFT, RIGHT, UP, DOWN = Moves['LEFT'].value, Moves['RIGHT'].value, Moves['UP'].value, Moves['DOWN'].value
# фишка в том, что когда сделаем меню, можно будет позволить игроку менять настройки управления, а в коде поменяются:
settings_body = (pg.K_a, pg.K_d, pg.K_w, pg.K_s) # это
settings_head = (pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5) # и это
directions_body = {settings_body[0]: (*LEFT, "LEFT"),
                   settings_body[1]: (*RIGHT, "RIGHT"),
                   settings_body[2]: (*UP, "UP"),
                   settings_body[3]: (*DOWN, "DOWN")}

directions_head = {settings_head[0]: "LEFT",
                   settings_head[1]: "RIGHT",
                   settings_head[2]: "UP",
                   settings_head[3]: "DOWN"}
###
# специально разбил, чтобы можно было создавать множество персонажей(понятно будет в следующих коммитах)
body_images_dict: dict = {"DOWN": [load_image(f'textures/heroes/body/forward/{i}.png') for i in range(10)],
                          "LEFT": [load_image(f'textures/heroes/body/left/{i}.png') for i in range(10)],
                          "RIGHT": [load_image(f'textures/heroes/body/right/{i}.png') for i in range(10)],
                          "UP": [load_image(f'textures/heroes/body/up/{i}.png') for i in range(10)]}

head_images_dict: dict = {"DOWN": load_image('textures/heroes/head/forward.png'),
                          "LEFT": load_image('textures/heroes/head/left.png'),
                          "RIGHT": load_image('textures/heroes/head/right.png'),
                          "UP": load_image('textures/heroes/head/up.png')}


#
class Body(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = body_images_dict["DOWN"][0]
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

        self.flag_move_down: bool = False
        self.flag_move_left: bool = False
        self.flag_move_right: bool = False
        self.flag_move_up: bool = False
        self.is_move: bool = False

    def settings(self):
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

    def setting_flags(self, key, is_down: bool): #left right up dow
        if key == settings_body[0]:
            self.flag_move_left = is_down
        elif key == settings_body[1]:
            self.flag_move_right = is_down
        elif key == settings_body[2]:
            self.flag_move_up = is_down
        elif key == settings_body[3]:
            self.flag_move_down = is_down

    # подумаю, как вынести в файл Animation.py
    def animating(self, name: str):
        peremennaya = self.indexes[name] + 1
        self.settings()
        self.indexes[name] = peremennaya % len(body_images_dict["DOWN"])
        self.image = body_images_dict[name][self.indexes[name]] if self.is_move else body_images_dict["DOWN"][0]


class Head(pg.sprite.Sprite):
    def __init__(self,
                 xy: tuple[int, int],
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...],):
        super().__init__()
        tear_class: Type[BaseTear] = BaseTear
        self.image = head_images_dict["DOWN"]
        self.is_rotated = False
        self.shot_ticks = 0
        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_speed = shot_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.tear_collide_groups = tear_collide_groups
        self.tears = pg.sprite.Group()
        self.x, self.y = xy[0], xy[1]

    def set_tear_collide_groups(self, tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]):
        self.tear_collide_groups = tear_collide_groups

    def update(self, delta_t, x, y) -> None:
        self.x, self.y = x, y
        self.tears.update(delta_t)
        self.shot_ticks += delta_t
        #print(self.x, self.y)
        if self.shot_ticks >= self.shot_delay and self.is_rotated:
            pass
            #self.shot()

    def shot(self) -> None:
        self.shot_ticks = 0
        size = self.image.get_size()
        coords_center_head: tuple[int, int] = self.x + size[0] // 2, self.y + size[1] // 2
        self.tear_class((self.x, self.y), coords_center_head, self.shot_damage, self.shot_max_distance, self.shot_speed,
                        self.shot_speed, self.tear_collide_groups, self.tears)

    # подумаю, как вынести в файл Animation.py
    def animating(self, direction: str):
        self.image = head_images_dict[direction] if self.is_rotated else head_images_dict["DOWN"]


# по факту - это родительский класс для песронажей( ГГ )
class Player(MoveSprite):
    def __init__(self,
                 pos_xy: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = (),
                 *groups: pg.sprite.AbstractGroup,
                 ):
        self.hp = hp
        self.damage_from_blow = damage_from_blow
        self.speed = 4
        super().__init__(pos_xy, ())
        self.body = Body()
        self.head = Head(pos_xy, shot_damage, shot_max_distance, shot_speed, shot_delay, tear_collide_groups)
        self.image = self.get_surf_gg()
        self.rect = self.image.get_rect()
        self.last_name_direction = "DOWN"
        self.count_cadrs = 0
        self.x, self.y = pos_xy

        ####
        self.vx, self.vy = self.speed, self.speed

    def update_room_groups(self, groups) -> None:
        hero_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = groups[0]
        tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = groups[1]
        #self.head.set_tear_collide_groups(tear_collide_groups)
        # РАСКОММЕНТИРУЙ НИЖНЮЮ СТРОЧКУ
        # self.collide_groups = hero_collide_groups

    def set_flags_move(self, event: pg.event.Event, is_keydown: bool):
        key = event.key
        if key in settings_body:
            self.body.setting_flags(key, is_keydown)

        elif key in settings_head:
            self.head.is_rotated = is_keydown
            self.rotation_head(directions_head[key])

    def update(self, delta_t):
        #print("AAAAAAAAAA", self.x, self.y)
        self.count_cadrs += 1
        self.head.update(delta_t, self.x, self.y)
        self.step_out_body(delta_t)
        self.image = self.get_surf_gg()

# MoveSprite move collides
    def get_surf_gg(self) -> pg.Surface:
        surf = pg.Surface((50, 50), pg.SRCALPHA, 32)
        surf = surf.convert_alpha()
        size = self.body.image.get_size()
        coords = (25 - size[0] // 2, 56 - size[1])
        surf.blit(self.body.image, coords)
        size = self.head.image.get_size()
        surf.blit(self.head.image, (25 - size[0] // 2, 25 - size[1] + 13))
        return surf

    def move_cooord(self, delta_t):
        dx, dy = 0, 0
        if self.body.flag_move_up:
            dy -= self.speed
        if self.body.flag_move_down:
            dy += self.speed
        if self.body.flag_move_right:
            dx += self.speed
        if self.body.flag_move_left:
            dx -= self.speed
        self.body.is_move = dx != 0 or dy != 0

        if dy != 0:
            self.last_name_direction = "UP" if dy < 0 else "DOWN"
        elif dx != 0:
            self.last_name_direction = "LEFT" if dx < 0 else "RIGHT"

        dx *= CELL_SIZE * delta_t
        dy *= CELL_SIZE * delta_t
        if dx != 0 and dy != 0:
            dx *= 0.7 # cos 45
            dy *= 0.7 # cos 45
        #MoveSprite.check_collides(self)
        return dx, dy

    # перемещение
    def step_out_body(self, delta_t):
        dx, dy = self.move_cooord(delta_t)
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y
        #self.check_collides()
        if self.count_cadrs % 3 == 0:
            self.body.animating(self.last_name_direction)

    # поворот головы
    def rotation_head(self, name_direction):
        self.head.animating(name_direction)
###
