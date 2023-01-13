import pygame as pg

from src.utils.funcs import load_font


class BaseFont:
    """
    Класс шрифта.

    :param name: Путь до файла, начиная от src/data, e.g. "font/prices.png"
    :param alphabet: Буквы по порядку с картинки шрифта.
    :param columns: Количество столбцов.
    :param rows: Количество строк.
    :param total: Сколько всего букв (если есть пустые клетки).
    :param scale_sizes: До каких размеров scale'ить (ширина, высота)
    """

    def __init__(self,
                 name: str,
                 alphabet: str,
                 columns: int,
                 rows: int,
                 total: int = None,
                 scale_sizes: tuple[int, int] = None):
        self.letters = load_font(name, columns, rows, total=total, scale_sizes=scale_sizes)
        self.alphabet = alphabet

        assert len(self.letters) == len(alphabet), "Неверно введены буквы или неверно указан путь до шрифта"

    def write_text(self, text: str) -> pg.Surface:
        """
        Написать текст.

        :param text: Что написать
        :return: Поверхность с этим текстом.
        """

        text = text.lower()
        width, height = self.letters[0].get_size()
        surface = pg.Surface((len(text) * width, height), pg.SRCALPHA, 32)

        for i, symb in enumerate(text):
            try:
                surface.blit(self.letters[self.alphabet.index(symb)],
                             (i * width, 0))
            except IndexError:
                raise IndexError(f'В шрифте с буквами "{self.alphabet}" нет буквы "{symb}')

        return surface

    def place_text(self, screen: pg.Surface, text: str | pg.Surface, xy_center: tuple[int, int]):
        """
        Нанести текст на экран.

        :param screen: На что наносить.
        :param text: Что наносить.
        :param xy_center: Центр куда наносить.
        """

        if isinstance(text, str):
            text = self.write_text(text)

        x, y = xy_center
        x -= text.get_width() // 2
        y -= text.get_height() // 2
        screen.blit(text, (x, y))
