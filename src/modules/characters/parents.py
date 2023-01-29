import random

import pygame as pg

from typing import Type
from src.utils.funcs import cell_to_pixels, get_direction, load_image, crop, load_sound
from src.modules.animations.Animation import Animation
from src.consts import CELL_SIZE, ROOM_WIDTH, ROOM_HEIGHT, GAME_OVER, GG_HURT, Moves, HeartsTypes
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Based.BaseTear import BaseTear


class TexturesHeroes:
    """
    Класс текстур для героя.
    """
    textures: dict[str, dict] = {
        name:
            {'body':
                {"DOWN": [crop(load_image(f'textures/heroes/body/forward/{name}_{i}.png')) for i in range(10)],
                 "LEFT": [crop(load_image(f'textures/heroes/body/left/{name}_{i}.png')) for i in range(10)],
                 "RIGHT": [crop(load_image(f'textures/heroes/body/right/{name}_{i}.png')) for i in range(10)],
                 "UP": [crop(load_image(f'textures/heroes/body/up/{name}_{i}.png')) for i in range(10)],
                 "death": crop(load_image(f'textures/heroes/death/{name}.png'))
                 },
             'head':
                {"DOWN": crop(load_image(f'textures/heroes/head/{name}_forward.png')),
                 "LEFT": crop(load_image(f'textures/heroes/head/{name}_left.png')),
                 "RIGHT": crop(load_image(f'textures/heroes/head/{name}_right.png')),
                 "UP": crop(load_image(f'textures/heroes/head/{name}_up.png'))}
             }
        for name in ('isaac', 'cain', 'lost')
    }


class ParamsHeroes(TexturesHeroes):
    """
    Класс настроек ГГ.
    """
    settings_body: list[int] = [pg.K_a, pg.K_d, pg.K_w, pg.K_s]                # настройки движения ГГ
    # settings_head: list[int] = [pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5]    # настройки поворота головы
    settings_head: list[int] = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]    # настройки поворота головы

    directions_head = {settings_head[0]: "LEFT",
                       settings_head[1]: "RIGHT",
                       settings_head[2]: "UP",
                       settings_head[3]: "DOWN"}
    body_images_dict: dict | None  # Словарь текстурок движения тела. Ключ - Направление, значение - список изображений.
    head_images_dict: dict | None  # Словарь текстурок поворота головы. Ключ - Направление, значение - изображение.
    characterizations: dict[str, dict] = {
        'isaac': {
            'hp': 6,
            'speed': 4,
            'damage': 2,
            'is_flying': False,
            'offset': 10
        },
        'cain': {
            'hp': 4,
            'speed': 6,
            'damage': 3,
            'is_flying': False,
            'offset': 10
        },
        'lost': {
            'hp': 1,
            'speed': 4,
            'damage': 2,
            'is_flying': True,
            'offset': 18
        }
    }     # Словарь базовых характеристик персонажей. Ключ - имя персонажа

    def set_images(self, name: str):
        """
        Настройка изображений героя, в зависимости от его имени.

        :param name: имя ГГ.
        """
        self.body_images_dict = self.textures[name]['body']
        self.head_images_dict = self.textures[name]['head']

    def get_characters(self, name: str):
        """
        Выдача начальных характеристик героя, в зависимости от его имени.

        :param name: имя ГГ.
        :return: список хп, скорость, урон, летающий/не летающий, смещение головы по оси 0y относительно тела
        """
        return self.characterizations[name].values()

    def set_move_params(self, body: list[int], head: list[int]):
        """
        Настройка управления (боди - ходьба, хед - стрельба).

        :param body: настройки передвижения (тело).
        :param head: настройки поворота головы.
        """
        self.settings_body = body
        self.settings_head = head


class Head(pg.sprite.Sprite):
    """
    Класс головы персонажа.

    :param shot_damage: настройки передвижения(тело).
    :param tears: слёзы.
    :param params: настройки поворота, изображения.
    """
    shot_max_distance: int | float = 5
    shot_speed: int | float = 5
    shot_delay: int | float = 0.5
    tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]

    def __init__(self,
                 shot_damage: int | float,
                 tears: pg.sprite.AbstractGroup,
                 params: ParamsHeroes):
        super().__init__()

        self.shot_ticks: float = 0                           # время с прошлого выстрела
        self.shot_damage: float = shot_damage                # урон
        self.vx_tear: float = 0                              # скорость слезы по оси 0x
        self.vy_tear: float = 0                              # скорость слезы по оси 0y
        self.player_speed: tuple[float, float] = 0, 0        # текущая скорость персонажа(для отклонения пули при беге)

        self.tears = tears
        self.tear_class: Type[BaseTear] = HeroTear

        self.is_rotated = False   # повёрнута ли голова

        self.last_name_direction: str = "DOWN"      # последнее направление головы (по сути, последняя нажатая кнопка)
        self.on_directions: list[str, ...] = []     # список активных направлений (по сути, список нажатых кнопок)

        self.params_hero = params
        self.image = self.params_hero.head_images_dict["DOWN"]
        self.rect = pg.Rect((0, 0, self.image.get_width(), self.image.get_height()))

    def set_tear_collide_groups(self, tear_collide_groups: tuple[pg.sprite.AbstractGroup, ...]):
        """
        Настройка групп, в которые может врезаться слеза.

        :param tear_collide_groups: кортеж групп, в которые может врезаться слеза.
        """
        self.tear_collide_groups = tear_collide_groups

    def settings_vx_vy_tear(self):
        """
        Настройки скоростей слезы.
        """
        if self.is_rotated:
            if self.last_name_direction in ["LEFT", "RIGHT"]:
                self.vx_tear = self.shot_speed if self.last_name_direction == "RIGHT" else -self.shot_speed
                # if self.player_speed[1] != 0:
                self.vy_tear += self.player_speed[1] * 0.3  # константа выведена практически
            elif self.last_name_direction in ["UP", "DOWN"]:
                self.vy_tear = self.shot_speed if self.last_name_direction == "DOWN" else -self.shot_speed
                # if self.player_speed[0] != 0:
                self.vx_tear += self.player_speed[0] * 0.3  # константа выведена практически

    def set_player_speed(self, vx: int | float, vy: int | float):
        """
        Сохранение(не изменяет!) скорости персонажа(нужно для отклонения пули при движении).

        :param vx: скорость по оси 0x.
        :param vy: скорость по оси 0y.
        """
        self.vy_tear, self.vx_tear = 0, 0
        self.player_speed = vx, vy

    def update(self, delta_t) -> None:
        """
        Обновление кадра.

        :param delta_t: время с прошлого кадра.
        """
        self.shot_ticks += delta_t
        if self.shot_ticks >= self.shot_delay and self.is_rotated:
            self.shot()
        self.tears.update(delta_t)

    def shot(self) -> None:
        """
        Стрельба.
        """
        self.shot_ticks = 0
        self.settings_vx_vy_tear()
        self.tear_class((0, 0), self.rect.center, int(self.shot_damage), self.shot_max_distance,
                        self.vx_tear, self.vy_tear, self.tear_collide_groups, self.tears)

    def set_directions(self, direction: str, is_down: bool):
        self.on_directions.append(direction) if is_down else self.on_directions.remove(direction)
        if self.on_directions:
            self.last_name_direction, self.is_rotated = self.on_directions[-1], True
        else:
            self.last_name_direction, self.is_rotated = "DOWN", False
        self.animating()

    def animating(self):
        """
        Поворот головы.
        """
        self.image = self.params_hero.head_images_dict[self.last_name_direction]

    def draw_tears(self, screen: pg.Surface):
        """
        Рисовка слёз.
        """
        self.tears.draw(screen)


class Player(MoveSprite):
    """
    Класс ГГ.

    :param name: имя выбранного персонажа.
    """
    death: pg.Surface | None = None
    death_sound = load_sound("sounds/isaac_death2.mp3")  # перенести
    hurt_sounds: list[pg.mixer.Sound] = [load_sound(f"sounds/isaac_hurt{i}.mp3") for i in range(1, 4)]

    a: float = 0.35  # Ускорение. Выведено практически

    def __init__(self, name: str):

        center_room = ROOM_WIDTH // 2, ROOM_HEIGHT // 2
        super().__init__(center_room, (), acceleration=self.a)
        self.params_hero = ParamsHeroes()
        self.params_hero.set_images(name)
        self.death = self.params_hero.body_images_dict['death']

        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}  # кол-во кадров, прошедших в определённую сторону

        self.tears = pg.sprite.Group()  # слёзы
        self.max_red_hp, self.max_speed, damage, self.is_flying, self.offset = self.params_hero.get_characters(name)
        self.head = Head(damage, self.tears, self.params_hero)  # голова персонажа

        self.collide_groups: tuple[pg.sprite.AbstractGroup, ...] | None = None  # группы, в которые может врезаться ГГ
        self.player_sprites = pg.sprite.LayeredUpdates()
        self.player_sprites.add(self, layer=1)
        self.player_sprites.add(self.head, layer=2)

        # разное
        self.damage_from_blow: int = 1                  # урон от бомбы самому себе
        self.count_cadrs: int = 0                       # кол-во прошедших кадров (нужно для анимации)
        self.score: int = 0                             # кол-во очков

        # здоровье
        self.red_hp: int = self.max_red_hp              # кол-во красных хп(половинки сердца)
        self.blue_hp: int = 0                           # аналогично красным, только синие
        self.black_hp: int = 0                          # аналогично красным, только чёрные

        self.count_bombs: int = 3                       # кол-во бомб
        self.count_key: int = 0                         # кол-во ключей
        self.count_money: int = 10                       # кол-во монет

        # таймеры
        self.use_bombs_delay: int | float = 1           # интервал между активациями бомб
        self.use_bombs_ticks: float = 0                 # время с прошлой активации бомбы
        self.timer_hurt: float = 2                      # интервал между получением урона
        self.timer: float = 2                           # время с прошлого получения урона
        self.score_sub_tick: float = 1                  # интервал снятия очков
        self.score_sub_timer: float = 0                 # время с прошлого снятия очков

        # флаги движения
        self.flag_move_down: bool = False               # вниз
        self.flag_move_left: bool = False               # влево
        self.flag_move_right: bool = False              # вправо
        self.flag_move_up: bool = False                 # вверх
        self.is_move: bool = False                      # движется ли ГГ
        self.is_alive: bool = True                      # живой ли персонаж

        # флаги коллизии
        self.x_collide: bool = False                    # коллизия произошла слева или справа
        self.y_collide: bool = False                    # коллизия произошла сверху или снизу

        # флаги направления
        self.last_name_direction: str = "DOWN"          # в прошлый кадр анимация была в эту сторону
        self.move_last_direction: str | None = None     # в прошлый кадр ГГ двигался в эту сторону

        self.image = self.params_hero.body_images_dict["DOWN"][0]
        self.image = crop(self.image)
        size = max(self.image.get_width(), self.image.get_height())
        self.rect = pg.Rect((0, 0, size, size))

        self.soul = Soul()                              # душа ГГ

    def hurt(self, damage: int):
        """
        Получение урона.

        :param damage: полученный урон.
        """
        if self.timer > self.timer_hurt:
            if self.blue_hp:
                self.blue_hp -= damage
            elif self.black_hp:
                self.black_hp -= damage
            else:
                self.red_hp -= damage
            self.timer = 0
            if self.red_hp > 0:
                random.choice(Player.hurt_sounds).play()
            pg.event.post(pg.event.Event(GG_HURT))

    def kill_tears(self):
        """
        Убийство слёз(при переходе между комнатами).
        """
        self.head.tears.empty()

    def update_timer(self, delta_t):
        """
        Обновление таймеров.

        :param delta_t: время с прошлого кадра.
        """
        self.timer += delta_t
        self.score_sub_timer += delta_t
        if self.score_sub_timer >= self.score_sub_tick:
            self.score -= 1
            self.score_sub_timer -= self.score_sub_tick

    def blow(self):
        """
        Получение урона при взрыве бомбы.
        """
        self.hurt(self.damage_from_blow)

    def setting_flags(self, key, is_down: bool):
        """
        Настройка флагов движения.

        :param key: ключ нажатой/отпущенной кнопки.
        :param is_down: нажата ли кнопка.
        """

        if key == self.params_hero.settings_body[0]:
            self.flag_move_left = is_down
        elif key == self.params_hero.settings_body[1]:
            self.flag_move_right = is_down
        elif key == self.params_hero.settings_body[2]:
            self.flag_move_up = is_down
        elif key == self.params_hero.settings_body[3]:
            self.flag_move_down = is_down

    def animating(self):
        """
        Анимация движения.
        """
        if self.count_cadrs == 0:
            last_name = self.last_name_direction
            peremennaya = self.indexes[last_name] + 1
            self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0,
                            last_name: peremennaya % len(self.params_hero.body_images_dict["DOWN"])}

            if self.is_move:
                self.image = self.params_hero.body_images_dict[last_name][self.indexes[last_name]]
            else:
                self.image = self.params_hero.body_images_dict["DOWN"][0]

    def settings_move_speed(self, delta_t: float):
        """
        Настройка скоростей движения, в зависимости от нажатых клавиш.

        :param delta_t: время с прошлого кадра.
        """
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
        """
        Коллизия с чем-то.

        :param other: то, с чем произошла коллизия.
        """
        if not MoveSprite.collide(self, other):
            return

        if isinstance(other, BaseTear) and other not in self.tears.sprites():
            self.hurt(other.damage)
            other.destroy()

    def reset_collides(self):
        """
        Сброс флагов коллизии.
        """
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

    def update_room_groups(self, required_groups, hero_collide_groups, tear_collide_groups) -> None:
        """
        Обновление групп коллизий при переходе в другую комнату / этаж.

        :param required_groups: группа коллизий для летающего персонажа.
        :param hero_collide_groups: группа коллизий для ходячего персонажа.
        :param tear_collide_groups: группы, в которые может врезаться слеза ГГ.
        """
        self.head.set_tear_collide_groups(tear_collide_groups)
        self.collide_groups = required_groups if self.is_flying else hero_collide_groups

    def pickup_heart(self, count: int, heart_type: HeartsTypes) -> bool:
        """
        Поднятие сердца.

        :param count: кол-во поднятых хп.
        :param heart_type: какой тип сердца.
        :return: True - сердце возможно поднять. False - хп полное.
        """
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

    def is_buy(self, count: int, price: int, heart_type: HeartsTypes | None) -> bool:
        """
        Покупка предмета.

        :param count: кол-во поднятых хп.
        :param price: цена.
        :param heart_type: какой тип сердца.
        :return: True - покупка успешна. False - невозможно купить.
        """
        if self.count_money >= price:
            if heart_type:
                if not self.pickup_heart(count, heart_type):
                    return False
            self.count_money -= price
            return True
        return False

    def move_to_cell(self, xy_pos):
        """
        Перемещение ГГ в нужную клетку при переходе в другую комнату.

        :param xy_pos: координаты клетки.
        """
        x, y = cell_to_pixels(xy_pos)
        self.x_center = x
        self.x_center_last = x
        self.y_center = y
        self.y_center_last = y
        self.vx, self.vy = 0, 0

    def set_flags_move(self, event: pg.event.Event, is_down: bool):
        """
        Настройка флагов движения.

        :param event: нажатая кнопка.
        :param is_down: True - кнопка нажата. False - кнопка отпущена.
        """
        key = event.key
        if key in self.params_hero.settings_body:
            self.setting_flags(key, is_down)

        elif key in self.params_hero.settings_head:
            self.head.set_directions(self.params_hero.directions_head[key], is_down)

    def reset_speed(self):
        """
        Сброс флагов и скоростей.
        """
        self.flag_move_up = False
        self.flag_move_left = False
        self.flag_move_right = False
        self.flag_move_down = False
        self.vx, self.vy = 0, 0

    def update(self, delta_t: float):
        """
        Обновление кадра.

        :param delta_t: время с прошлого кадра.
        """
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
            self.head.rect.center = coords[0], coords[1] - self.offset
            # self.offset выведена на практике(чтобы голова выглядела нормально)
        else:
            if self.is_alive:
                self.image = self.death
                self.player_sprites.remove(self.head)
                self.soul.set_coords(self.rect.center)
                Player.death_sound.play()
            self.is_alive = False
            self.soul.update(delta_t)
            if self.soul.is_end_animation():
                pg.event.post(pg.event.Event(GAME_OVER, {'score': self.score}))

    def activate_bombs(self) -> bool:
        """
        Активация бомбы.

        :return: True - бомба активирована. False - не хватает бомб или вы недавно использовали.
        """
        if self.count_bombs > 0 and self.use_bombs_ticks > self.use_bombs_delay:
            self.count_bombs -= 1
            self.use_bombs_ticks = 0
            return True
        return False

    def scoring_points(self, counts: int):
        """
        Подсчёт очков.

        :param counts: кол-во очков.
        """
        self.score += counts

    def get_speed(self) -> tuple[int, int]:
        """
        Возвращает скорости персонажа.

        :return: кортеж скоростей(сначала по оси 0x, потом по оси 0y).
        """
        return self.vx, self.vy

    def render(self, screen: pg.Surface):
        """
        Отрисовка персонажа и его слёз.

        :param screen: полотно, на котором нужно нарисовать.
        """
        self.player_sprites.draw(screen)
        self.head.draw_tears(screen)
        if not self.is_alive:
            self.soul.render(screen)


class Soul(pg.sprite.Sprite):
    """
    Класс души.
    """
    start_image = load_image('textures/heroes/soul/soul0.png')
    images = load_image('textures/heroes/soul/move_soul.png')
    fps_animation = 15

    def __init__(self):
        super().__init__()
        self.image = self.start_image
        self.animation = Animation(self.images, 10, 1, self.fps_animation, False)
        self.xy_pos: tuple[int, int] | None = None  # текущие координаты (х, у)
        self.start_x_pos: int | None = None         # стартовая координата по оси 0x
        self.vx, self.vy = -50, -50                 # скорости
        self.timer: int | float = 3                 # длительность анимации

    def set_coords(self, xy_pos: tuple[int, int]):
        """
        Настройка начальной точки души.

        :param xy_pos: кортеж координат смерти(x, y).
        """
        self.xy_pos = xy_pos
        self.start_x_pos = xy_pos[0]

    def is_end_animation(self) -> bool:
        """
        Закончилась ли анимация смерти.

        :return: True -  анимация закончилась. False - ещё нет.
        """
        return self.timer <= 0

    def update(self, delta_t):
        """
        Обновление кадра.

        :param delta_t: время с прошлого кадра.
        """
        if self.timer > 0:
            self.animation.update(delta_t)
            self.image = self.animation.image
            self.move(delta_t)
            self.timer -= delta_t

    def move(self, delta_t):
        """
        Перемещение души.

        :param delta_t: время с прошлого кадра.
        """
        if self.xy_pos[0] <= self.start_x_pos - CELL_SIZE // 4 or self.xy_pos[0] >= self.start_x_pos + CELL_SIZE // 4:
            self.vx *= -1
        self.xy_pos = self.xy_pos[0] + self.vx * delta_t, self.xy_pos[1] + self.vy * delta_t

    def render(self, screen: pg.Surface):
        """
        Отрисовка души.

        :param screen: полотно, на котором нужно нарисовать.
        """
        if self.timer > 0:
            screen.blit(self.image, self.xy_pos)


class HeroTear(BaseTear):
    """
    Класс слезы ГГ.

    :param xy_pos: Позиция в комнате.
    :param xy_pixels: Координата спавна в пикселях, центр слезы.
    :param damage: Урон.
    :param max_distance: Дальности полёта в клетках (переделывается в pixels/sec).
    :param vx: Скорость по горизонтали в клетках (переделывается в pixels/sec).
    :param vy: Скорость по вертикали в клетках (переделывается в pixels/sec).
    :param collide_groups: Группы, с которыми надо проверять столкновение.
    :param groups: Группы спрайтов.
    :param is_friendly: Игнорирует ли главного героя.
    """
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
        """
        Настройка изображения слезы.
        """
        max_size = len(BaseTear.all_tears[0]) - 1
        self.image = crop(BaseTear.all_tears[0][min(int(self.damage + 2), max_size)])
