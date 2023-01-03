import pygame as pg

from src.modules.BaseClasses.MovableItem import MovableItem
from src.utils.funcs import load_image, load_sound
from src.consts import PICKUP_LOOT


class PickBomb(MovableItem):
    """
    Подбираемая бомба.

    :param xy_pos: Позиция в комнате.
    :param main_hero: Главный герой.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param groups: Группы спрайтов.
    """

    bomb: pg.Surface = load_image("textures/room/bomb.png")
    pickup_sound = load_sound("soundes/penny_pickup.mp3")

    def __init__(self,
                 xy_pos: tuple[int, int],
                 main_hero: pg.sprite.Sprite,
                 collide_groups: tuple[pg.sprite.AbstractGroup, ...],
                 *groups: pg.sprite.AbstractGroup):
        acceleration: int | float = 1
        pickable = True
        super().__init__(xy_pos, acceleration, collide_groups, *groups, pickable=pickable)

        self.main_hero = main_hero
        self.set_image()
        self.set_rect()

    def set_image(self):
        self.image = PickBomb.bomb

    def update(self, delta_t: float):
        super().move(delta_t)
        if pg.sprite.collide_rect(self, self.main_hero):
            self.pickup()

    def pickup(self):
        """
        Подбор бомбы.
        """
        PickBomb.pickup_sound.play()
        pg.event.post(pg.event.Event(PICKUP_LOOT, {'item': PickBomb}))
        self.kill()

