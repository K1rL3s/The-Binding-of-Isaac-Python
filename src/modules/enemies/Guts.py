import pygame as pg

from src.modules.BaseClasses.Based.MoveSprite import MoveSprite
from src.modules.BaseClasses.Enemies.MovingEnemy import MovingEnemy
from src.modules.animations.Animation import Animation
from src.utils.funcs import load_image


class Guts(MovingEnemy):
    """
    Мозго-органная каша, которая котается по полу.

    :param xy_pos: Позиция в комнате.
    :param room_graph: Граф комнаты.
    :param enemy_collide_groups: Группы спрайтов, с которыми нужно обрабатывать столкновения этой сущности.
    :param groups: Группы спрайтов.
    """

    images = load_image("textures/enemies/guts.png")
    fps = 15

    def __init__(self,
                 xy_pos: tuple[int, int],
                 room_graph: dict[tuple[int, int]],
                 enemy_collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        main_hero = pg.sprite.Sprite()
        hp = 10
        speed = 2.5
        damage_from_blow = 10
        move_update_delay = 1
        MovingEnemy.__init__(self, xy_pos, hp, speed, damage_from_blow, move_update_delay,
                             room_graph, main_hero, enemy_collide_groups, *groups)

        self.vx, self.vy = -self.speed, 0
        self.animation = Animation(Guts.images, 4, 4, Guts.fps, total_frames=12, frame=-1)
        self.image = self.animation.image

        self.do_update_speed = False

        self.set_rect()

    def move_back(self, rect: pg.Rect):
        MovingEnemy.move_back(self, rect)
        centerx, centery = rect.center

        if self.rect.centery < centery and self.vy > 0:
            self.vx, self.vy = self.speed, 0
        elif self.rect.centery > centery and self.vy < 0:
            self.vx, self.vy = -self.speed, 0
        elif self.rect.centerx < centerx and self.vx > 0:
            self.vx, self.vy = 0, -self.speed
        elif self.rect.centerx > centerx and self.vx < 0:
            self.vx, self.vy = 0, self.speed

    def update(self, delta_t: float):
        MovingEnemy.update(self, delta_t)
        self.animation.update(delta_t)
        self.image = self.animation.image

    def collide(self, other: MoveSprite):
        MovingEnemy.collide(self, other)

        # Изменить на ГГ!!!
        if isinstance(other, MoveSprite):
            other.hurt(1)
            other.move_back(self.rect)
