import pygame as pg

from src import consts
from src.utils.funcs import load_image, load_sound
from src.modules.levels.Room import Room


def main():
    pg.init()
    pg.font.init()
    pg.mixer.init()
    screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))

    all_textures = {
        "rooms": {
            "controls": pg.Surface((0, 0)),
            consts.FloorsTypes.BASEMENT: load_image("textures/room/basement.png"),
            consts.FloorsTypes.CAVES: load_image("textures/room/basement.png"),
            consts.FloorsTypes.CATACOMBS: load_image("textures/room/basement.png"),
            consts.FloorsTypes.DEPTHS: load_image("textures/room/basement.png"),
            consts.FloorsTypes.BLUEWOMB: load_image("textures/room/basement.png"),
            consts.FloorsTypes.WOMB: load_image("textures/room/basement.png"),
            consts.RoomsTypes.TREASURE: load_image("textures/room/basement.png"),
            consts.RoomsTypes.SHOP: load_image("textures/room/basement.png"),
            consts.RoomsTypes.SECRET: load_image("textures/room/basement.png"),
        },
        "rocks": {
            "alive": load_image("textures/room/rocks.png"),
            "destroy_animation": None,
        }
    }

    all_sounds = {
        "fart": load_sound("sounds/fart.mp3"),
        "rock_crumble": [
            load_sound("sounds/rock_crumble1.wav"),
            load_sound("sounds/rock_crumble2.wav"),
            load_sound("sounds/rock_crumble3.wav"),
        ],
    }

    room = Room(consts.FloorsTypes.WOMB, consts.RoomsTypes.DEFAULT, 1, (0, 0), None, all_textures, all_sounds)

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

    pg.quit()


if __name__ == '__main__':
    main()
