import pygame as pg

from src import consts

pg.init()
pg.font.init()
pg.mixer.init()
pg.key.set_repeat(50, 50)
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))

from src.modules.Game import Game
from src.modules.mainmenu import startscrean
from src.utils.funcs import load_sound


def main():
    pg.mixer.music.load(load_sound('sounds/main_theme.mp3', return_path=True))
    pg.mixer.music.play()
    startscrean.start_screen(screen)
    game = Game(screen)
    game.background = pg.Color(27, 24, 24)
    pg.mixer.music.stop()
    game.setup()
    game.start()
    pg.quit()


if __name__ == '__main__':
    main()
