import pygame as pg

from src.modules.BaseClasses.Based.BaseTear import BaseTear
from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.utils.funcs import load_sound
from src.modules.BaseClasses.Based.BaseSprite import BaseSprite
from src.modules.characters.parents import Player


class BaseEnemy(BaseSprite):
    """
    Базовый класс противника.

    :param xy_pos: Позиция спавна в клетках.
    :param hp: Здоровье.
    :param damage_from_blow: Урон получаемый от взрывов.
    :param room_graph: Графоподобный словарь клеток в комнате.
    :param main_hero: Главный персонаж (у него должен быть .rect)
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param groups: Группы спрайтов.
    """

    explosion_kill = load_sound("sounds/explosion_kill.mp3")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 hp: int,
                 damage_from_blow: int,
                 room_graph: dict[tuple[int, int]],
                 main_hero: Player,
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        BaseSprite.__init__(self, xy_pos, *groups)
        self.groups = groups

        self.hp = hp
        self.damage_from_blow = damage_from_blow
        self.room_graph = room_graph
        self.main_hero = main_hero
        self.enemy_collide_groups = enemy_collide_groups
        self.image: pg.Surface
        self.rect: pg.Rect
        self.mask: pg.mask.Mask = pg.mask.Mask((0, 0))

    def blow(self):
        """
        Взрыв сущности.
        """
        self.hurt(self.damage_from_blow)
        if self.hp <= 0:
            BaseEnemy.explosion_kill.play()

    def hurt(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.death()

    def update_room_graph(self, room_graph: dict[tuple[int, int]]):
        """
        Обновление графа комнаты (например, после ломания Poop'a).

        :param room_graph: Графоподобный словарь клеток комнаты.
        """
        self.room_graph = room_graph

    def death(self):
        """
        Смерть врага.
        """
        self.kill()

    def collide(self, other: MoveSprite):
        if isinstance(other, BaseTear):
            self.hurt(other.damage)
            other.destroy()
            return True
        return False
