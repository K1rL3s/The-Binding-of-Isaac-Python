import random

import pygame as pg

from src.consts import CELL_SIZE
from src.utils.funcs import load_image, load_sound
from src.modules.BaseClasses.BaseItem import BaseItem


class Poop(BaseItem):
    """
    Класс Poop'a.

    :param xy_pos: Позиция в комнате.
    :param poop_group: Группа спрайтов, где все спрайты - Poop'ы.
    :param collidable_group: Группа спрайтов, где все спрайты - препятствия.
    :param *groups: Остальные группы спрайтов.
    :param collidable: Можно ли столкнуться с объектом (непроходимый ли).
    """

    poops: pg.Surface = load_image("textures/room/poops.png")
    poop_destoryed = [load_sound("sounds/pop1.wav"), load_sound("sounds/pop2.mp3")]

    max_hp = 10

    def __init__(self,
                 xy_pos: tuple[int, int],
                 collidable_group: pg.sprite.AbstractGroup,
                 *groups: pg.sprite.AbstractGroup,
                 collidable: bool = True):
        BaseItem.__init__(self, xy_pos, collidable_group, *groups, collidable=collidable)

        self.collidable_group = collidable_group

        self.stages: list[pg.Surface] = []
        self.treasure: list[BaseItem] = []
        self.hp = Poop.max_hp

        self.set_image()
        self.set_rect(CELL_SIZE, CELL_SIZE)

    def set_image(self):
        poop_type = random.choices(list(range(0, 5)), [0.90, 0.045, 0.045, 0.005, 0.005])[0]
        # Добавить лут в self.treasure, если текстурка из последних двух
        texture_x = poop_type * CELL_SIZE
        self.stages = [Poop.poops.subsurface(texture_x, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) for y in range(5)]
        self.image = self.stages[0]

    def blow(self):
        """
        Взрыв Poop'a.
        """
        self.hurt(self.hp)

    def hurt(self, damage: int):
        """
        Нанесение урона Poop'y.

        :param damage: сколько урона.
        """
        if not self.hp:
            return
        self.hp = max(0, self.hp - damage)
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
        self.image = self.stages[4]
        self.collidable = False
        self.collidable_group.remove(self)
        random.choice(self.poop_destoryed).play()
        self.drop_something()

    def drop_something(self):
        """
        Выпадение лута после поломки.
        """
        if self.treasure:
            pass
        elif random.random() > 0.9:
            pass
