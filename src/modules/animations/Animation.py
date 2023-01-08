import pygame as pg


class Animation:
    """
    Класс для воспроизведения анимаций.

    :param sheet: Surface, который обрезается на кадры.
    :param columns: Кол-во кадров в длине.
    :param rows: Количество кадров в высоте.
    :param fps: Скорость анимации.
    :param single_play: Проиграть анимацию один раз.
    :param scale_sizes: К каким размерам scale'ить кадр.
    :param frame: С какого кадра начинать.
    """
    def __init__(self,
                 sheet: pg.Surface,
                 columns: int,
                 rows: int,
                 fps: int,
                 single_play: bool = False,
                 scale_sizes: tuple[int, int] = None,
                 frame: int = 0):
        self.frames: list[pg.Surface] = []
        self.rect = pg.Rect(0, 0, 0, 0)
        self.cut_sheet(sheet, columns, rows, scale_sizes=scale_sizes)

        self.cur_frame = frame
        self.image = self.frames[self.cur_frame]

        self.ticks_counter = 0
        self.frame_delimiter = 1 / fps
        self.single_play = single_play

    def cut_sheet(self, sheet: pg.Surface, columns: int, rows: int, scale_sizes: tuple[int, int] = None):
        self.rect = pg.Rect(
            0, 0,
            sheet.get_width() // columns,
            sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)

                part = sheet.subsurface(pg.Rect(frame_location, self.rect.size))
                if scale_sizes:
                    part = pg.transform.scale(part, scale_sizes)
                self.frames.append(part)

        real_size = self.frames[0].get_size()
        self.rect = pg.Rect(0, 0, *real_size)

    def reset(self):
        self.ticks_counter = 0
        self.cur_frame = 0

    def update(self, delta_t: float) -> bool | None:
        """
        Обновление кадра в анимации, если пришло его время.

        :param delta_t: Время с прошлого кадра.
        :return: Обновился ли кадр.
        """
        self.ticks_counter += delta_t

        if self.ticks_counter >= self.frame_delimiter:
            index = self.cur_frame + 1

            if self.single_play and index == len(self.frames):
                return None

            self.cur_frame = index % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.ticks_counter = 0

            return True

        return False
