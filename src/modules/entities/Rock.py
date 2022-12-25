import random

import pygame as pg

from src.consts import FloorsTypes, CELL_SIZE
from src.modules.entities.BaseEntity import BaseEntity
from src.modules.Animation import Animation


class Rock(BaseEntity):
    def __init__(self, xy_pos: tuple[int, int],
                 floor_type: FloorsTypes | str,
                 sounds: list[pg.mixer.Sound],
                 textures: dict[str, pg.Surface | dict[str, pg.Surface | list[pg.Surface]] | list[pg.Surface]],
                 rocks_group: pg.sprite.AbstractGroup,
                 collidable_group: pg.sprite.AbstractGroup,
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = True):
        super().__init__(xy_pos, sounds, textures, rocks_group, collidable_group, *groups, collidable=collidable)

        self.rocks_group = rocks_group
        self.collidable_group = collidable_group
        self.floor_type = floor_type
        self.with_treasure = False
        self.image = None
        self.destroyed_image = None
        self.rect = None
        self.set_image()
        self.set_rect()

    def update(self, delta_t: float, *args, **kwargs):
        """
        Камень не двигается...
        """
        pass

    def set_image(self):
        texture_x = 0
        texture_y = random.choices(list(range(1, 5)), [0.2375, 0.2375, 0.2375, 0.05])[0] * CELL_SIZE
        self.with_treasure = texture_y == CELL_SIZE * 4
        for i, floor_type in enumerate(FloorsTypes):
            if floor_type == self.floor_type:
                texture_x = i * CELL_SIZE
                break
        self.image = self.textures["alive"].subsurface((texture_x, texture_y, CELL_SIZE, CELL_SIZE))
        self.destroyed_image = self.textures["alive"].subsurface((texture_x, 0, CELL_SIZE, CELL_SIZE))

    def set_start_speed(self, *args, **kwargs):
        raise TypeError("Cannot move a Rock")

    def pickup(self, *args, **kwargs):
        raise TypeError("Cannot pickup a Rock")

    def hurt(self, *args, **kwargs):
        raise TypeError("Cannot hurt a Rock")

    def destroy(self):
        """
        Уничтожение камня после взрыва.
        """
        random.choice(self.sounds).play()
        self.image = self.destroyed_image
        self.collidable_group.remove(self)
        self.destroy_animation()

    def destroy_animation(self):
        # Разлёт частиц, которые удалятся после перезахода в комнату
        Animation(self.textures["destroy_animation"])
