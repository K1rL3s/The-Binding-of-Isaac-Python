import random

import pygame as pg

from src import consts


pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))


from src.modules.levels.Room import Room


def main():
    room = Room(random.choice(list(consts.FloorsTypes)), random.choice(list(consts.FloorsTypes)),
                random.randint(1, 4), (0, 0), None)

    running = True
    timer = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        delta_t = timer.tick(60) / 1000
        screen.fill(pg.Color('white'))
        room.render(screen)
        pg.display.flip()

        # Убрать эту строку, чтобы комнаты не менялись
        room = Room(random.choice(list(consts.FloorsTypes)), random.choice(list(consts.FloorsTypes)),
                  random.randint(1, 4), (0, 0), None)

    pg.quit()


if __name__ == '__main__':
    main()
