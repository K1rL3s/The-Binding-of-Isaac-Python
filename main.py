import pygame as pg

from src import consts
from src.utils.funcs import create_data_base

pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))

from src.modules.game import Game, start_game


def main():
    create_data_base()
    while True:
        name = start_game(screen)
        game = Game(name, screen)
        game.background = pg.Color(27, 24, 24)
        pg.mixer.music.stop()
        game.setup()
        game.start()
    # pg.quit()


if __name__ == "__main__":
    main()
