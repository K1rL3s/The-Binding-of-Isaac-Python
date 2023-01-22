import random

import pygame as pg

from src.utils.funcs import cut_sheet


class Animation:
    """
    Класс для воспроизведения анимаций.

    :param sheet: Surface, который обрезается на кадры.
    :param columns: Кол-во кадров в длине.
    :param rows: Количество кадров в высоте.
    :param fps: Скорость анимации.
    :param single_play: Проиграть анимацию один раз.
    :param scale_sizes: К каким размерам scale'ить кадр.
    :param frame: С какого кадра начинать, -1 - с рандомного.
    """
    def __init__(self,
                 sheet: pg.Surface,
                 columns: int,
                 rows: int,
                 fps: int,
                 single_play: bool = False,
                 scale_sizes: tuple[int, int] = None,
                 frame: int = 0,
                 total_frames: int = None):
        self.frames = cut_sheet(sheet, columns, rows, scale_sizes=scale_sizes, total=total_frames)
        self.rect = pg.Rect(0, 0, *self.frames[0].get_size())

        self.cur_frame = frame if frame != -1 else random.randint(0, len(self.frames) - 1)
        self.image = self.frames[self.cur_frame]

        self.ticks_counter = 0
        self.frame_delimiter = 1 / fps
        self.single_play = single_play

    def reset(self):
        self.ticks_counter = 0
        self.cur_frame = 0

    def update(self, delta_t: float) -> bool | None:
        """
        Обновление кадра в анимации, если пришло его время.

        :param delta_t: Время с прошлого кадра.
        :return: True - кадр обновился. False - кадр не обновился. None - одноразовая анимация кончилась.
        """
        self.ticks_counter += delta_t

        if self.ticks_counter >= self.frame_delimiter:
            self.ticks_counter = 0

            index = self.cur_frame + 1

            if self.single_play and index == len(self.frames):
                return None

            self.cur_frame = index % len(self.frames)
            self.image = self.frames[self.cur_frame]

            return True

        return False
