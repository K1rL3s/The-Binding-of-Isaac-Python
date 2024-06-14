import random

import pygame as pg

from src.consts import CELL_SIZE
from src.modules.base_classes import DestroyableItem
from src.utils.funcs import load_image, load_sound


class Poop(DestroyableItem):
    """
    Класс Poop'a.

    :param xy_pos: Позиция в комнате.
    :param *groups: Остальные группы спрайтов.
    :param collidable: Можно ли столкнуться с объектом (непроходимый ли).
    """

    poops: pg.Surface = load_image("textures/room/poops.png")
    poop_destoryed = [load_sound("sounds/pop1.wav"), load_sound("sounds/pop2.mp3")]

    max_hp = 10

    def __init__(
        self,
        xy_pos: tuple[int, int],
        *groups: pg.sprite.AbstractGroup,
        collidable: bool = True,
    ):
        DestroyableItem.__init__(self, xy_pos, *groups, collidable=collidable)

        self.stages: list[pg.Surface] = []
        self.hp = Poop.max_hp

        self.set_image()
        self.set_rect(CELL_SIZE, CELL_SIZE)

    def set_image(self):
        poop_type = random.choices(
            list(range(5)),
            [0.90, 0.045, 0.045, 0.005, 0.005],
        )[0]
        # Добавить лут в self.treasure, если текстурка из последних двух
        texture_x = poop_type * CELL_SIZE
        self.stages = [
            Poop.poops.subsurface(texture_x, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for y in range(5)
        ]
        self.image = self.stages[0]

    def hurt(self, damage: int):
        """
        Нанесение урона Poop'y.

        :param damage: сколько урона.
        """
        if not DestroyableItem.hurt(self, damage):
            return

        percent = self.hp / Poop.max_hp
        if percent >= 0.75:
            self.image = self.stages[0]
        elif percent >= 0.5:
            self.image = self.stages[1]
        elif percent >= 0.25:
            self.image = self.stages[2]
        elif percent > 0:
            self.image = self.stages[3]
        else:
            self.destroy()

    def destroy(self):
        """
        Уничтожение Poop после взрыва/поломки.
        """
        DestroyableItem.destroy(self)
        self.image = self.stages[4]
        random.choice(self.poop_destoryed).play()
