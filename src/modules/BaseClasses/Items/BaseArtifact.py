import pygame as pg

from src.modules.BaseClasses import MoveSprite


class BaseArtifact(MoveSprite):
    """
    Класс артефакта, который летает над пьедесталом.

    :param xy_pos: Позиция в комнате (пьедестала),
    :param groups: Группы спрайтов.
    :param xy_pixels: Позиция в пикселях.
    """

    fly_speed = 0.1  # Скорость движения вверх-вниз в клетках/секунду
    change_direction_delay = 2

    def __init__(self,
                 xy_pixels: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup):
        MoveSprite.__init__(self, (0, 0), (), *groups,
                            acceleration=0, xy_pixels=xy_pixels)

        self.set_speed(0, -BaseArtifact.fly_speed)
        self.change_direction_ticks = 0

        self.set_image()
        self.set_rect()

    def update(self, delta_t: float):
        self.change_direction_ticks += delta_t
        if self.change_direction_ticks >= BaseArtifact.change_direction_delay:
            self.change_direction_ticks = 0
            self.set_speed(0, -self.vy)
        self.move(delta_t)
