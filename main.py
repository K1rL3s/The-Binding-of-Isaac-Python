import random

import pygame as pg

from src import consts


pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))


from src.modules.levels.Room import Room


def main():
    room = Room(random.choice(list(consts.FloorsTypes)), consts.RoomsTypes.SPAWN,
                random.randint(1, 4), (0, 0), None)
    running = True
    timer = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                room = Room(random.choice(list(consts.FloorsTypes)), random.choice(list(consts.RoomsTypes)),
                            random.randint(1, 4), (0, 0), None)
                print(room.floor_type, room.room_type)
        delta_t = timer.tick(60) / 1000
        screen.fill(pg.Color('white'))
        room.update(delta_t)
        room.render(screen)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
