import random
from typing import Type

import pygame as pg

from src.consts import PICKUP_ART, CELL_SIZE
from src.utils.funcs import load_image, load_sound
from src.modules.BaseClasses import PickableItem, BaseArtifact


class Pedestal(PickableItem):
    """
    Класс пьедестала, на котором стоит артефакт.

    :param xy_pos: Позиция пьедестала в комнате.
    :param collide_groups: Группы спрайтов, через спрайты которых нельзя пройти.
    :param artifacts_group: Группа спрайтов, где все спрайты - артефакты.
    :param groups: Группы спрайтов.
    """

    pedestal = load_image("textures/room/altars.png").subsurface(0, 0, CELL_SIZE, CELL_SIZE)
    pick_sound = [load_sound(f"sounds/powerup{i}.mp3") for i in range(1, 5)]

    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups: pg.sprite.AbstractGroup,
                 artifacts_group: pg.sprite.AbstractGroup = None,
                 artifact: Type[BaseArtifact] = None):
        PickableItem.__init__(self, xy_pos, *groups, collidable=True)

        self.image = Pedestal.pedestal
        self.set_rect()
        self.pick_sound = Pedestal.pick_sound

        self.artifact: BaseArtifact | None = None
        self.set_artifact(artifact, artifacts_group)

    def set_artifact(self, artifact: Type[BaseArtifact] | None, artifacts_group: pg.sprite.AbstractGroup | None):
        """
        Установка артефакта на пьедестал.

        :param artifact: Артефакт.
        :param artifacts_group: Группа спрайтов, где все спрайты - артефакты.
        """
        if artifact:
            assert isinstance(artifacts_group, pg.sprite.AbstractGroup)
            self.artifact = artifact(self.rect.midtop, artifacts_group)

    def update(self, delta_t: float):
        """
        Анимация артефакта (перемещение вверх-вниз) происходит внутри артефакта.

        :param delta_t: Время с прошлого кадра.
        """
        if self.artifact:
            self.artifact.update(delta_t)

    def blow(self):
        """
        ВРЕМЕННЫЙ МЕТОД ДЛЯ ТЕСТА!!! УДАЛИТЬ!!!
        """
        self.pickup()

    def pickup(self):
        """
        Подбор предмета.
        """
        if not self.artifact:
            return

        if isinstance(self.pick_sound, pg.mixer.Sound):
            self.pick_sound.play()
        elif isinstance(self.pick_sound, list):
            random.choice(self.pick_sound).play()

        pg.event.post(pg.event.Event(PICKUP_ART, {
                                                 'item': self.artifact,
                                                 'self': self
                                                 }
                                     )
                      )

        self.artifact.kill()
        self.artifact = None
