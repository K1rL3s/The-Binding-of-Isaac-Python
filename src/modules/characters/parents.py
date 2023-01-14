import pygame as pg

from src.utils.funcs import crop, cell_to_pixels
from src.modules.animations.Animation import Animation
from typing import Type
from src.utils.funcs import load_image
from src.consts import CELL_SIZE
from src.consts import Moves
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear
#from src.modules.entities.tears.ExampleTear import ExampleTear

# фишка в том, что когда сделаем меню, можно будет позволить игроку менять настройки управления, а в коде поменяются:
settings_body = (pg.K_a, pg.K_d, pg.K_w, pg.K_s)  # это
settings_head = (pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5)  # и это
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


class Body(MoveSprite):
    def __init__(self, hp, tears: pg.sprite.AbstractGroup):
        super().__init__((1, 0), (), acceleration=0)
        self.hp = hp
        self.tears = tears
        self.damage_from_blow: int = 10
        self.image = body_images_dict["DOWN"][0]
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

        self.collide_groups: tuple[pg.sprite.AbstractGroup, ...] | None = None

        self.flag_move_down: bool = False
        self.flag_move_left: bool = False
        self.flag_move_right: bool = False
        self.flag_move_up: bool = False
        self.is_move: bool = False

        # Заменить get_width и get_height на что-то типа cell_size // 2, или cell_size / 3 * 2, типо того
        # и смотреть, чтобы голова не съехала
        self.rect = pg.Rect((0, 0, self.image.get_width(), self.image.get_height()))

    def hurt(self, damage):
        self.hp -= damage

    def blow(self):
        self.hurt(self.damage_from_blow)

    def settings(self):
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

    def setting_flags(self, key, is_down: bool):
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

    def check_collides(self):
        if self.collide_groups:
            MoveSprite.check_collides(self)

    def collide(self, other):
        if isinstance(other, BaseTear) and other not in self.tears.sprites():
            self.hurt(other.damage)
            other.destroy()
        MoveSprite.collide(self, other)


class Head(pg.sprite.Sprite):
    def __init__(self,
                 xy_pix: tuple[int, int],
                 tears: pg.sprite.AbstractGroup,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...], ):
        super().__init__()
        tear_class: Type[BaseTear] = HeroTear
        self.image = head_images_dict["DOWN"]
        self.is_rotated = False
        self.is_shot = False
        self.shot_ticks = 0
        self.shot_damage = shot_damage
        self.shot_max_distance = shot_max_distance
        self.shot_speed = shot_speed
        self.shot_delay = shot_delay
        self.tear_class = tear_class
        self.tear_collide_groups = tear_collide_groups
        self.tears = tears
        self.player_speed: tuple[int | float, int | float] = 0, 0
        self.vx_tear: int | float = 0
        self.vy_tear: int | float = 0
        self.last_name_direction = "DOWN"
        self.rect = pg.Rect((xy_pix[0], xy_pix[1], self.image.get_width(), self.image.get_height()))

    def set_tear_collide_groups(self, tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]):
        self.tear_collide_groups = tear_collide_groups

    def settings_vx_vy_tear(self):
        if self.is_rotated:
            if self.last_name_direction in ["LEFT", "RIGHT"]:
                self.vx_tear = self.shot_speed if self.last_name_direction == "RIGHT" else -self.shot_speed
                #if self.player_speed[1] != 0:
                self.vy_tear += self.player_speed[1] * 0.3 # константа выведена практически
            elif self.last_name_direction in ["UP", "DOWN"]:
                self.vy_tear = self.shot_speed if self.last_name_direction == "DOWN" else -self.shot_speed
                #if self.player_speed[0] != 0:
                self.vx_tear += self.player_speed[0] * 0.3 # константа выведена практически

    def set_player_speed(self, vx: int | float, vy: int | float):
        self.vy_tear, self.vx_tear = 0, 0
        self.player_speed = vx, vy
        self.settings_vx_vy_tear()

    def update(self, delta_t) -> None:
        self.shot_ticks += delta_t
        if self.shot_ticks >= self.shot_delay and self.is_rotated:
            self.is_shot = True
            self.shot()
        self.tears.update(delta_t)

    def shot(self) -> None:
        self.shot_ticks = 0
        self.tear_class((0, 0), self.rect.center, self.shot_damage, self.shot_max_distance,
                        self.vx_tear, self.vy_tear, self.tear_collide_groups, self.tears)

    def animating(self, direction: str):
        self.image = head_images_dict[direction] if self.is_rotated else head_images_dict["DOWN"]
        self.last_name_direction = direction

    def draw_tears(self, screen: pg.Surface):
        self.tears.draw(screen)


# по факту - это родительский класс для песронажей( ГГ )
# Сделать сюда self.rect = self.body.rect, чтобы Player.rect ссылался на Body.rect, и после этого заменить все
# main_hero.body.rect на main_hero.rect
class Player:
    def __init__(self,
                 xy_pix: tuple[int, int],
                 hp: int,
                 speed_body,
                 damage_from_blow: int,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = (),
                 *groups: pg.sprite.AbstractGroup,
                 ):
        self.damage_from_blow = damage_from_blow
        self.max_speed = speed_body
        self.a = 0.01
        ################################################################################################
        self.speed = speed_body
        self.tears = pg.sprite.Group()
        self.body = Body(hp, self.tears)
        self.head = Head(xy_pix, self.tears, shot_damage, shot_max_distance, shot_speed, shot_delay, tear_collide_groups)
        self.last_name_direction = "DOWN"
        self.count_cadrs = 0
        self.body.rect.center = xy_pix
        self.rect = self.body.rect

        self.player_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites.add(self.body, layer=1)
        self.player_sprites.add(self.head, layer=2)

        self.vx, self.vy = self.speed, self.speed

    def update_room_groups(self, groups) -> None:
        hero_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = groups[0]
        tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = groups[1]
        self.head.set_tear_collide_groups(tear_collide_groups)
        self.body.collide_groups = hero_collide_groups

    def move_to_cell(self, xy_pos):
        x, y = cell_to_pixels(xy_pos)
        self.body.x_center = x
        self.body.x_center_last = x
        self.body.y_center = y
        self.body.y_center_last = y

    def set_flags_move(self, event: pg.event.Event, is_keydown: bool):
        key = event.key
        if key in settings_body:
            self.body.setting_flags(key, is_keydown)

        elif key in settings_head:
            self.head.is_rotated = is_keydown
            self.head.set_player_speed(*self.get_speed())
            self.rotation_head(directions_head[key])

    def update(self, delta_t):
        self.count_cadrs += 1
        self.head.set_player_speed(*self.get_speed())
        self.settings_move_speed(delta_t)
        self.step_out_body()

        self.head.update(delta_t)

        self.body.move(delta_t, use_a=False)
        self.body.check_collides()

        coords = self.body.rect.midtop
        self.head.rect.center = coords[0], coords[1] - 8 # константа выведена практически (чтобы голова выглядела норм)

    def settings_move_speed(self, delta_t):
        max_speed, a = self.max_speed, self.a * CELL_SIZE
        if (self.body.flag_move_up or self.body.flag_move_down) and \
            (self.body.flag_move_left or self.body.flag_move_right):
            max_speed *= 0.7
            a *= 0.7
        if self.body.flag_move_up:
            self.vy = max(-max_speed, self.vy - a * delta_t)
        elif self.vy < 0:
            self.vy = min(0, self.vy + a * delta_t)

        if self.body.flag_move_down:
            self.vy = min(max_speed, self.vy + a * delta_t)
        elif self.vy > 0:
            self.vy = max(0, self.vy - a * delta_t)

        if self.body.flag_move_left:
            self.vx = max(-max_speed, self.vx - a * delta_t)
        elif self.vx < 0:
            self.vx = min(0, self.vx + a * delta_t)

        if self.body.flag_move_right:
            self.vx = min(max_speed, self.vx + a * delta_t)
        elif self.vx > 0:
            self.vx = max(0, self.vx - a * delta_t)

        if self.body.flag_move_up or self.body.flag_move_down:
            self.last_name_direction = "UP" if self.body.flag_move_up else "DOWN"
        elif self.body.flag_move_right or self.body.flag_move_left:
            self.last_name_direction = "LEFT" if self.body.flag_move_left else "RIGHT"

        self.body.is_move = self.vx != 0 or self.vy != 0
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7  # cos 45
        #     self.vy *= 0.7  # sin 45

    def get_speed(self):
        # vx, vy = 0, 0
        # if self.body.flag_move_up:
        #     vy -= self.speed
        # if self.body.flag_move_down:
        #     vy += self.speed
        # if self.body.flag_move_right:
        #     vx += self.speed
        # if self.body.flag_move_left:
        #     vx -= self.speed
        # self.body.is_move = vx != 0 or vy != 0
        #
        # if vy != 0:
        #     self.last_name_direction = "UP" if vy < 0 else "DOWN"
        # elif vx != 0:
        #     self.last_name_direction = "LEFT" if vx < 0 else "RIGHT"
        #
        # if vx != 0 and vy != 0:
        #     vx *= 0.7  # cos 45
        #     vy *= 0.7  # sin 45

        return self.vx, self.vy

    # перемещение
    def step_out_body(self):
        self.body.set_speed(*self.get_speed())
        if self.count_cadrs % 3 == 0:
            self.body.animating(self.last_name_direction)

    # поворот головы
    def rotation_head(self, name_direction):
        # скорость головы надо сделать
        self.head.animating(name_direction)

    def render(self, screen: pg.Surface):
        self.player_sprites.draw(screen)
        self.head.draw_tears(screen)


class HeroTear(BaseTear):
    pop_animation = BaseTear.all_ends.subsurface(0, BaseTear.height, BaseTear.width, BaseTear.height)
    fps_animation = 30

    def __init__(self,
                 xy_pos: tuple[int, int],
                 xy_pixels: tuple[int, int],
                 damage: int,
                 max_distance: int | float,
                 vx: int | float,
                 vy: int | float,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        is_friendly = True
        BaseTear.__init__(self, xy_pos, xy_pixels, damage, max_distance, vx, vy, collide_groups, *groups,
                          is_friendly=is_friendly)

        self.animation = Animation(HeroTear.pop_animation, 16, 1, self.fps_animation, True)
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = crop(BaseTear.all_tears[1][5])
        self.mask = pg.mask.from_surface(self.image)