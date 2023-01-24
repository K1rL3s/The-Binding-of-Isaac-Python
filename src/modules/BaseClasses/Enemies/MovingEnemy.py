import math

import pygame as pg

from src.modules.BaseClasses.Enemies.BaseEnemy import BaseEnemy
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.characters.parents import Body
from src.modules.levels.Border import Border
from src.utils.funcs import pixels_to_cell, cell_to_pixels
from src.utils.graph import make_path_to_cell


class MovingEnemy(BaseEnemy, MoveSprite):
    """
    Противник ходящий.

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param speed: Скорость в клетках.
    :param damage_from_blow: Урон получаемый от взрывов.
    :param move_update_delay: Задержка между перерасчётом пути до ГГ.
    :param room_graph: Графоподобный словарь клеток в комнате.
    :param main_hero: Главный персонаж (у него должен быть .rect)
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param groups: Группы спрайтов.
    """

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 speed: int | float,
                 damage_from_blow: int,
                 move_update_delay: int | float,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Body | pg.sprite.Sprite,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup,
                 flyable: bool = False):
        BaseEnemy.__init__(self, xy_pos, hp, damage_from_blow, room_graph, main_hero, enemy_collide_groups, *groups)
        MoveSprite.__init__(self, xy_pos, enemy_collide_groups, *groups, acceleration=0)

        self.speed = speed
        self.move_update_delay = move_update_delay
        self.move_ticks = 0
        self.slowdown_coef: float = 1.0
        self.flyable = flyable
        self.path: list[tuple[int, int]] = []

        self.do_update_speed = True

    def update(self, delta_t: float):
        """
        Обновление врага, отмер времени для выстрела или движения.

        :param delta_t: Время с прошлого кадра.
        """
        BaseEnemy.update(self, delta_t)
        MoveSprite.update(self, delta_t)

        self.move_ticks += delta_t

        if self.move_ticks >= self.move_update_delay:
            self.update_move_speed()

        self.move(delta_t)

    def move(self, delta_t: float, change_speeds: bool = True):
        """
        Перемещение сущности.

        :param delta_t: Время с прошлого кадра.
        :param change_speeds: Вызывать ли update_move_speed().
        """
        MoveSprite.move(self, delta_t)

        # Проверка коллизий
        if self.flyable:
            self.check_fly_collides()
        else:
            MoveSprite.check_collides(self)

        # Если координаты есть и если они отличаются от текущих, то обновляем скорости
        xy_cell = pixels_to_cell((self.x_center, self.y_center))
        if xy_cell and (self.x, self.y) != xy_cell:
            self.x, self.y = xy_cell
            if change_speeds:
                self.update_move_speed()

    def move_back(self, rect: pg.Rect):
        """
        Обработка коллизии и изменение скоростей для обхода препятствия.

        :param rect: Центр спрайта, с которым было столкновение
        """
        MoveSprite.move_back(self, rect)

    def update_move_speed(self):
        """
        Обновление вертикальной и горизонатальной скоростей для перемещения к ГГ.
        """
        if not self.do_update_speed:
            self.move_ticks = 0
            return

        if self.flyable:  # Летающие летят напрямую ахахаха)
            dx = self.main_hero.rect.centerx - self.rect.centerx
            dy = self.main_hero.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance:
                self.set_speed(self.speed * dx / distance, self.speed * dy / distance)
            else:
                self.set_speed(0, 0)
            return

        self.move_ticks = 0
        xy_end = self.main_hero.rect.center
        xy_end = pixels_to_cell(xy_end)
        path_list = make_path_to_cell(self.room_graph, (self.x, self.y), xy_end)
        if not path_list or len(path_list) < 2:
            self.vx, self.vy = 0, 0
            return

        self.path = path_list[1:]
        next_cell = self.path[0]
        x, y = cell_to_pixels(next_cell)
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance:
            self.set_speed(self.speed * dx / distance, self.speed * dy / distance)

    def check_fly_collides(self):
        for group in self.collide_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    # Добавлять сюда то, с чем должны сталкиваться летающие
                    if sprite != self and isinstance(sprite, (Border,)):
                        sprite: Border
                        sprite.collide(self)
