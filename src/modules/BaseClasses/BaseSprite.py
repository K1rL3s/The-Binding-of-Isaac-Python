import pygame as pg


class BaseSprite(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, delta_t: float):
        """
        Обновление положения/счётчиков.

        :param delta_t: Время с прошлого кадра.
        """
        pass

    def set_image(self):
        """
        Установка текстурки.
        """
        pass

    def set_rect(self):
        """
        Установка rect и, иногда, mask
        """
        pass

    def hurt(self, damage: int):
        """
        Получение урона.
        """
        pass

    def blow(self):
        """
        Получение урона от взрыва.
        """
        pass

    def collide(self, other: pg.sprite.Sprite):
        """
        Обработка столкновений.

        :param other: наследник BaseSprite
        """
        pass

    def move_back(self, xy_center: tuple[int, int]):
        """
        Перемещение назад при столкновении.
        """
        pass
