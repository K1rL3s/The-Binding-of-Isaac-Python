import random

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.animations.animation import Animation
from src.modules.base_classes import BaseSprite, MovableItem, MoveSprite
from src.modules.characters.main_hero import Player
from src.utils.funcs import crop, load_image, load_sound


class BlowBomb(MovableItem):
    """
    Взрываемая бомба.

    :param xy_pos: Позиция в комнате.
    :param collide_groups: Группа препятствий, через которые нельзя пройти.
    :param blow_groups: Группы спрайтов, где все спрайты взрываются.
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    """

    bomb = crop(load_image("textures/room/bomb.png").subsurface(0, 0, 48, 48))
    bomb_animation = load_image("textures/room/bomb_explosion.png")
    explosion_sounds: list[pg.mixer.Sound] = [
        load_sound(f"sounds/explosion{i}.mp3") for i in range(1, 4)
    ]

    explosion_delay: int | float = 2.5  # Задержка перед взрывом в секундах
    collide_by_player_delay: int | float = (
        0.5  # Задержка перед тем, как будут обрабатываться столкновения с ГГ
    )
    explosion_radius: int | float = 1.25 * CELL_SIZE  # Радиус взрыва в пикселях
    explosion_fps: int = 30

    def __init__(
        self,
        xy_pos: tuple[int, int],
        collide_groups: tuple[pg.sprite.AbstractGroup, ...],
        blow_groups: tuple[pg.sprite.AbstractGroup, ...],
        *groups: pg.sprite.AbstractGroup,
        xy_pixels: tuple[int, int] = None,
    ):
        MovableItem.__init__(self, xy_pos, collide_groups, *groups, xy_pixels=xy_pixels)

        self.blow_groups = blow_groups
        self.ticks = 0
        self.blowed = False
        self.animation = Animation(
            BlowBomb.bomb_animation,
            4,
            4,
            BlowBomb.explosion_fps,
            True,
        )
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = BlowBomb.bomb

    def update(self, delta_t: float):
        """
        :param delta_t: Время с прошлого кадра.
        """
        if self.blowed:
            self.animation.update(delta_t)
            self.image = self.animation.image
        else:
            MovableItem.move(self, delta_t)
            self.ticks += delta_t
            if self.ticks >= BlowBomb.explosion_delay:
                self.blow_up()

    def collide(self, other: MoveSprite):
        if isinstance(other, Player) and self.ticks < self.collide_by_player_delay:
            return
        MovableItem.collide(self, other)

    def blow_up(self):
        """
        Подрыв себя.
        """
        self.blowed = True
        center = self.rect.center

        self.rect = pg.Rect(
            (0, 0, BlowBomb.explosion_radius * 2, BlowBomb.explosion_radius * 2),
        )
        self.rect.center = self.x_center, self.y_center
        for group in self.blow_groups:
            if sprites := pg.sprite.spritecollide(self, group, False):
                for sprite in sprites:
                    if sprite != self and pg.sprite.collide_circle(self, sprite):
                        sprite: BaseSprite
                        sprite.collide(self)
                        sprite.blow()
        random.choice(BlowBomb.explosion_sounds).play()

        self.image = self.animation.image
        self.rect = self.animation.rect
        self.rect.midbottom = center
        self.rect.bottom += CELL_SIZE // 2
