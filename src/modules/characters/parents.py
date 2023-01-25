import pygame as pg

from src.utils.funcs import cell_to_pixels, get_direction
from src.modules.animations.Animation import Animation
from typing import Type
from src.utils.funcs import load_image, crop, load_sound
from src.consts import CELL_SIZE, ROOM_WIDTH, ROOM_HEIGHT, GAME_OVER, GG_HURT
from src.consts import Moves, HeartsTypes

from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear

# from src.modules.entities.tears.ExampleTear import HeroTear


class TexturesHeroes:
    textures: dict[str, dict] = {
        name:
            {'body':
                {"DOWN": [crop(load_image(f'textures/heroes/body/forward/{name}_{i}.png')) for i in range(10)],
                 "LEFT": [crop(load_image(f'textures/heroes/body/left/{name}_{i}.png')) for i in range(10)],
                 "RIGHT": [crop(load_image(f'textures/heroes/body/right/{name}_{i}.png')) for i in range(10)],
                 "UP": [crop(load_image(f'textures/heroes/body/up/{name}_{i}.png')) for i in range(10)]},
             'head':
                {"DOWN": crop(load_image(f'textures/heroes/head/{name}_forward.png')),
                 "LEFT": crop(load_image(f'textures/heroes/head/{name}_left.png')),
                 "RIGHT": crop(load_image(f'textures/heroes/head/{name}_right.png')),
                 "UP": crop(load_image(f'textures/heroes/head/{name}_up.png'))}
             }
        for name in ('isaac',)  # eсли не запускается, нет изображений, то уберите cain/lost
    }


class ParamsHeroes(TexturesHeroes):
    settings_body: list[pg.event.Event] = [pg.K_a, pg.K_d, pg.K_w, pg.K_s]
    settings_head: list[pg.event.Event] = [pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5]
    directions_head = {settings_head[0]: "LEFT",
                       settings_head[1]: "RIGHT",
                       settings_head[2]: "UP",
                       settings_head[3]: "DOWN"}
    body_images_dict: dict | None
    head_images_dict: dict | None

    def set_images(self, name: str):
        self.body_images_dict = self.textures[name]['body']
        self.head_images_dict = self.textures[name]['head']

    def set_params(self, body: list[pg.event.Event],
                   head: list[pg.event.Event]):
        self.settings_body = body
        self.settings_head = head


class Head(pg.sprite.Sprite):
    def __init__(self,
                 name: str,
                 tears: pg.sprite.AbstractGroup,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...], params: ParamsHeroes):
        super().__init__()
        self.name = name
        self.params_hero = params
        tear_class: Type[BaseTear] = HeroTear
        self.image = self.params_hero.head_images_dict["DOWN"]
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
        self.rect = pg.Rect((0, 0, self.image.get_width(), self.image.get_height()))

        self.is_rotated = False
        self.on_directions = []

    def set_tear_collide_groups(self, tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]):
        self.tear_collide_groups = tear_collide_groups

    def settings_vx_vy_tear(self):
        if self.is_rotated:
            if self.last_name_direction in ["LEFT", "RIGHT"]:
                self.vx_tear = self.shot_speed if self.last_name_direction == "RIGHT" else -self.shot_speed
                # if self.player_speed[1] != 0:
                self.vy_tear += self.player_speed[1] * 0.3  # константа выведена практически
            elif self.last_name_direction in ["UP", "DOWN"]:
                self.vy_tear = self.shot_speed if self.last_name_direction == "DOWN" else -self.shot_speed
                # if self.player_speed[0] != 0:
                self.vx_tear += self.player_speed[0] * 0.3 # константа выведена практически

    def set_player_speed(self, vx: int | float, vy: int | float):
        self.vy_tear, self.vx_tear = 0, 0
        self.player_speed = vx, vy

    def update(self, delta_t) -> None:
        self.shot_ticks += delta_t
        if self.shot_ticks >= self.shot_delay and self.is_rotated:
            self.is_shot = True
            self.shot()
        self.tears.update(delta_t)

    def set_damage(self):
        self.shot_damage += 1

    def shot(self) -> None:
        self.shot_ticks = 0
        self.settings_vx_vy_tear()
        self.tear_class((0, 0), self.rect.center, self.shot_damage, self.shot_max_distance,
                        self.vx_tear, self.vy_tear, self.tear_collide_groups, self.tears)

    def set_directions(self, direction: str, is_keydown: bool):
        self.on_directions.append(direction) if is_keydown else self.on_directions.remove(direction)
        if self.on_directions:
            self.last_name_direction, self.is_rotated = self.on_directions[-1], True
        else:
            self.last_name_direction, self.is_rotated = "DOWN", False
        self.animating()

    # поворот головы
    def animating(self):
        self.image = self.params_hero.head_images_dict[self.last_name_direction]

    def draw_tears(self, screen: pg.Surface):
        self.tears.draw(screen)


# по факту - это родительский класс для песронажей( ГГ )
class Player(MoveSprite):
    death = load_image("death_isaac (2) (1).png")
    use_bombs_delay: int | float = 1

    def __init__(self,
                 name: str,
                 hp: int,
                 speed_body,
                 damage_from_blow: int,
                 shot_damage: int | float,
                 shot_max_distance: int | float,
                 shot_speed: int | float,
                 shot_delay: int | float,
                 tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...] = (),
                 ):
        center_room = ROOM_WIDTH // 2, ROOM_HEIGHT // 2
        self.params_hero = ParamsHeroes()
        self.params_hero.set_images(name)
        self.damage_from_blow = damage_from_blow
        self.a = 0.35
        self.count_bombs = 10
        self.count_key = 0
        self.speed = 2
        self.count_money: int = 0
        super().__init__(center_room, (), acceleration=self.a)

        self.tears = pg.sprite.Group()
        self.head = Head(name, self.tears, shot_damage + 5, shot_max_distance, shot_speed, shot_delay,
                         tear_collide_groups, self.params_hero)
        self.count_cadrs = 0
        self.soul: Soul = Soul()
        self.is_alive = True
        self.use_bombs_ticks = 0

        self.player_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites.add(self, layer=1)
        self.player_sprites.add(self.head, layer=2)

        # self.vx, self.vy = 0, 0
        #################

        self.name = name
        self.red_hp = hp
        self.max_red_hp = hp
        self.blue_hp = 0
        self.black_hp = 0

        self.max_speed = speed_body
        self.damage_from_blow: int = 10
        self.image = self.params_hero.body_images_dict["DOWN"][0]
        self.image = crop(self.image)
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}
        self.timer_hurt: float = 2
        self.timer: float = 2

        self.collide_groups: tuple[pg.sprite.AbstractGroup, ...] | None = None

        self.flag_move_down: bool = False
        self.flag_move_left: bool = False
        self.flag_move_right: bool = False
        self.flag_move_up: bool = False
        self.is_move: bool = False

        self.x_collide = False
        self.y_collide = False

        self.last_name_direction: str = "DOWN"
        self.move_last_direction: str | None = None

        size = max(self.image.get_width(), self.image.get_height())
        self.rect = pg.Rect((0, 0, size, size))

    def hurt(self, damage):
        if self.timer > self.timer_hurt:
            if self.blue_hp:
                self.blue_hp -= damage
            elif self.black_hp:
                self.black_hp -= damage
            else:
                self.red_hp -= damage
            self.timer = 0
            pg.event.post(pg.event.Event(GG_HURT))

    def update_timer(self, delta_t):
        self.timer += delta_t

    def blow(self):
        self.hurt(self.damage_from_blow)

    def settings(self):
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

    def setting_flags(self, key, is_down: bool):
        if key == self.params_hero.settings_body[0]:
            self.flag_move_left = is_down
        elif key == self.params_hero.settings_body[1]:
            self.flag_move_right = is_down
        elif key == self.params_hero.settings_body[2]:
            self.flag_move_up = is_down
        elif key == self.params_hero.settings_body[3]:
            self.flag_move_down = is_down

    def animating(self):
        if self.count_cadrs == 0:
            last_name = self.last_name_direction
            peremennaya = self.indexes[last_name] + 1
            self.settings()
            self.indexes[last_name] = peremennaya % len(self.params_hero.body_images_dict["DOWN"])
            if self.is_move:
                self.image = self.params_hero.body_images_dict[last_name][self.indexes[last_name]]
            else:
                self.image = self.params_hero.body_images_dict["DOWN"][0]

    def settings_move_speed(self, delta_t):
        max_speed, a = self.max_speed, self.a * CELL_SIZE
        if (self.flag_move_up or self.flag_move_down) and not \
                (self.flag_move_up and self.flag_move_down) and \
                (self.flag_move_left or self.flag_move_right) and not \
                (self.flag_move_left and self.flag_move_right) and not \
                (self.x_collide or self.y_collide):
            max_speed *= 0.7  # cos 45
            a *= 0.7  # sin 45

        if self.flag_move_up and not self.flag_move_down and not self.y_collide:
            self.vy = max(-max_speed, self.vy - a * delta_t)
        elif self.vy < 0:
            self.vy = min(0, self.vy + a * delta_t)

        if self.flag_move_down and not self.flag_move_up and not self.y_collide:
            self.vy = min(max_speed, self.vy + a * delta_t)
        elif self.vy > 0:
            self.vy = max(0, self.vy - a * delta_t)

        if self.flag_move_left and not self.flag_move_right and not self.x_collide:
            self.vx = max(-max_speed, self.vx - a * delta_t)
        elif self.vx < 0:
            self.vx = min(0, self.vx + a * delta_t)

        if self.flag_move_right and not self.flag_move_left and not self.x_collide:
            self.vx = min(max_speed, self.vx + a * delta_t)
        elif self.vx > 0:
            self.vx = max(0, self.vx - a * delta_t)

        if self.flag_move_up or self.flag_move_down:
            self.last_name_direction = "UP" if self.flag_move_up else "DOWN"
        elif self.flag_move_right or self.flag_move_left:
            self.last_name_direction = "LEFT" if self.flag_move_left else "RIGHT"

        self.is_move = self.vx != 0 or self.vy != 0

    def collide(self, other):
        if isinstance(other, BaseTear) and other not in self.tears.sprites():
            self.hurt(other.damage)
            other.destroy()
        MoveSprite.collide(self, other)

    def reset_collides(self):
        self.x_collide = self.y_collide = False

    def move_back(self, rect: pg.Rect):
        """
        Обработка коллизии и изменение скоростей при столкновении.

        :param rect: Rect того, с чем было столкновение.
        """
        direction = get_direction(self.rect, rect)

        self.y_collide = direction in (Moves.UP, Moves.DOWN) or self.y_collide
        self.x_collide = direction in (Moves.LEFT, Moves.RIGHT) or self.x_collide

        if direction == Moves.RIGHT and self.vx > 0:
            self.move_last_direction = "UP" if self.vy < 0 else "DOWN"
            if self.vy:
                self.vy = (-1 if self.vy < 0 else 1) * (abs(self.vy) + abs(self.vx * 0.7))
            self.vx = 0

        elif direction == Moves.LEFT and self.vx < 0:
            self.move_last_direction = "UP" if self.vy < 0 else "DOWN"
            if self.vy:
                self.vy = (-1 if self.vy < 0 else 1) * (abs(self.vy) + abs(self.vx * 0.7))
            self.vx = 0

        elif direction == Moves.UP and self.vy < 0:
            self.move_last_direction = "LEFT" if self.vx < 0 else "RIGHT"
            if self.vx:
                self.vx = (-1 if self.vx < 0 else 1) * (abs(self.vx) + abs(self.vy * 0.7))
            self.vy = 0

        elif direction == Moves.DOWN and self.vy > 0:
            self.move_last_direction = "LEFT" if self.vx < 0 else "RIGHT"
            if self.vx:
                self.vx = (-1 if self.vx < 0 else 1) * (abs(self.vx) + abs(self.vy * 0.7))
            self.vy = 0

        if direction in (Moves.TOPLEFT, Moves.TOPRIGHT) and self.vy < 0:
            self.y_collide = True
            if self.vx != 0:
                self.vy = 0
        if direction in (Moves.BOTTOMLEFT, Moves.BOTTOMRIGHT) and self.vy > 0:
            self.y_collide = True
            if self.vx != 0:
                self.vy = 0
        if direction in (Moves.TOPLEFT, Moves.BOTTOMLEFT) and self.vx < 0:
            self.x_collide = True
            if self.vy != 0:
                self.vx = 0
        if direction in (Moves.TOPRIGHT, Moves.BOTTOMRIGHT) and self.vx > 0:
            self.x_collide = True
            if self.vy != 0:
                self.vx = 0

        if self.x_collide:
            self.x_center = self.x_center_last
            self.rect.centerx = self.x_center
        if self.y_collide:
            self.y_center = self.y_center_last
            self.rect.centery = self.y_center

        if self.vx > self.max_speed:
            self.vx = self.max_speed
        elif self.vx < -self.max_speed:
            self.vx = -self.max_speed
        if self.vy > self.max_speed:
            self.vy = self.max_speed
        elif self.vy < -self.max_speed:
            self.vy = -self.max_speed

    def update_room_groups(self, hero_collide_groups, tear_collide_groups) -> None:
        self.head.set_tear_collide_groups(tear_collide_groups)
        self.collide_groups = hero_collide_groups

    def pickup_heart(self, count: int, heart_type: HeartsTypes) -> bool:
        if heart_type == HeartsTypes.RED:
            if self.red_hp >= self.max_red_hp:
                return False
            self.red_hp += count
            self.red_hp = min(self.red_hp, self.max_red_hp)
        elif heart_type == HeartsTypes.BLUE:
            self.blue_hp += count
        elif heart_type == HeartsTypes.BLACK:
            self.black_hp += count
        return True

    def is_buy(self, count: int, price: int,  heart_type: HeartsTypes | None) -> bool:
        if self.count_money >= price:
            if heart_type:
                print(self.red_hp)
                if not self.pickup_heart(count * 2, heart_type):
                    return False
            print(self.red_hp)
            self.count_money -= price
            print(self.count_money)
            return True
        return False

    def move_to_cell(self, xy_pos):
        x, y = cell_to_pixels(xy_pos)
        self.x_center = x
        self.x_center_last = x
        self.y_center = y
        self.y_center_last = y
        self.reset_speed()

    def set_flags_move(self, event: pg.event.Event, is_keydown: bool):
        key = event.key
        if key in self.params_hero.settings_body:
            self.setting_flags(key, is_keydown)

        elif key in self.params_hero.settings_head:
            self.head.set_directions(self.params_hero.directions_head[key], is_keydown)

    def reset_speed(self):
        self.flag_move_up = False
        self.flag_move_left = False
        self.flag_move_right = False
        self.flag_move_down = False
        self.vx, self.vy = 0, 0

    def set_damage(self):
        self.head.set_damage()

    def update(self, delta_t: float):
        if self.red_hp > 0:
            self.use_bombs_ticks += delta_t
            self.count_cadrs += 1
            self.count_cadrs %= 3

            self.animating()
            self.head.update(delta_t)
            self.move(delta_t, use_a=False)
            self.update_timer(delta_t)
            self.reset_collides()
            self.settings_move_speed(delta_t)
            self.check_collides()

            self.head.set_player_speed(*self.get_speed())
            coords = self.rect.midtop
            self.head.rect.center = coords[0], coords[1] - 8  # выведена на практике(чтобы голова выглядела нормально)
        else:
            if self.is_alive:
                self.image = self.death
                self.player_sprites.remove(self.head)
                self.soul.set_coords(self.rect.center)
            self.is_alive = False
            self.soul.update(delta_t)
            if self.soul.is_end_animation():
                pg.event.post(pg.event.Event(GAME_OVER))

    def get_count_bombs(self) -> bool:
        if self.count_bombs > 0 and self.use_bombs_ticks > self.use_bombs_delay:
            self.count_bombs -= 1
            self.use_bombs_ticks = 0
            return True
        return False

    def get_coords(self):
        return self.rect.center

    def get_speed(self) -> tuple[int, int]:
        return self.vx, self.vy

    def render(self, screen: pg.Surface):
        self.player_sprites.draw(screen)
        self.head.draw_tears(screen)
        if not self.is_alive:
            self.soul.render(screen)


class Soul(pg.sprite.Sprite):
    start_image = load_image('soul0.png')
    images = load_image('move_soul.png')
    fps_animation = 15

    def __init__(self):
        super().__init__()
        self.image = self.start_image
        self.animation = Animation(self.images, 10, 1, self.fps_animation, False)
        self.xy_pos: tuple[int, int] | None = None
        self.start_x_pos: int | None = None
        self.vx, self.vy = -50, -50
        self.timer: int | float = 3

    def set_coords(self, xy_pos: tuple[int, int]):
        self.xy_pos = xy_pos
        self.start_x_pos = xy_pos[0]

    def is_end_animation(self) -> bool:
        return self.timer <= 0

    def update(self, delta_t):
        if self.timer > 0:
            self.animation.update(delta_t)
            self.image = self.animation.image
            self.move(delta_t)
            self.timer -= delta_t

    def move(self, delta_t):
        if self.xy_pos[0] <= self.start_x_pos - CELL_SIZE // 4 or self.xy_pos[0] >= self.start_x_pos + CELL_SIZE // 4:
            self.vx *= -1
        self.xy_pos = self.xy_pos[0] + self.vx * delta_t, self.xy_pos[1] + self.vy * delta_t

    def render(self, screen: pg.Surface):
        if self.timer > 0:
            screen.blit(self.image, self.xy_pos)


class HeroTear(BaseTear):
    pop_animation = BaseTear.all_ends.subsurface(0, 0, BaseTear.width, BaseTear.height)
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
        max_size = len(BaseTear.all_tears[0]) - 1
        self.image = crop(BaseTear.all_tears[0][min(self.damage + 2, max_size)])


