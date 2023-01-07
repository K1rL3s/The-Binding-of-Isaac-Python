import pygame as pg

from src.utils.funcs import cell_to_pixels


class BaseSprite(pg.sprite.Sprite):
    """
    Базированный спрайт.

    :param xy_pos: Позиция в комнате.
    :param groups: Группы спрайтов
    """
    def __init__(self,
                 xy_pos: tuple[int, int],
                 *groups):
        pg.sprite.Sprite.__init__(self, *groups)

        self.x, self.y = xy_pos

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

    def set_rect(self, width: int = None, height: int = None):
        """
        Установка объекта в центре своей клетки.
        """
        try:  # ЗАТЫЧКА ДЛЯ ВРЕМЕННОГО ГГ!!! УБРАТЬ!!!
            self.rect = self.image.get_rect()
        except AttributeError:  # ЗАТЫЧКА ДЛЯ ВРЕМЕННОГО ГГ!!! УБРАТЬ!!!
            return  # ЗАТЫЧКА ДЛЯ ВРЕМЕННОГО ГГ!!! УБРАТЬ!!!
        if width:
            self.rect.width = width
        if height:
            self.rect.height = height
        self.rect.center = cell_to_pixels((self.x, self.y))

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

    def collide(self, other: pg.sprite.Sprite) -> bool:
        """
        Обработка столкновений.

        :param other: наследник BaseSprite
        :return: Будет ли столкновение (разные ли объекты).
        """
        return other != self
