import pygame as pg

from src import consts

pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))

from src.modules.Game import Game
from src.modules.mainmenu import startscrean
from src.utils.funcs import load_sound
from src.modules.Banners.BaseFont import BaseFont


def main():
    pg.mixer.music.load(load_sound('sounds/main_theme.mp3', return_path=True))
    pg.mixer.music.play()
    startscrean.start_screen(screen)
    game = Game()
    pg.mixer.music.stop()

    running = True
    timer = pg.time.Clock()
    background = pg.Color(27, 24, 24)

    print(len("abcdefghijklmnopqrstuvwxyz0123456789$%€=?+-_ "))
    font = BaseFont("fonts/upheaval.png", "abcdefghijklmnopqrstuvwxyz0123456789$%€=?+-_ ", 26, 2, total=45)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    game.move_to_next_room(consts.Moves.UP)
                elif event.key == pg.K_DOWN:
                    game.move_to_next_room(consts.Moves.DOWN)
                elif event.key == pg.K_RIGHT:
                    game.move_to_next_room(consts.Moves.RIGHT)
                elif event.key == pg.K_LEFT:
                    game.move_to_next_room(consts.Moves.LEFT)
                elif event.key == pg.K_SPACE:
                    game.move_to_next_level()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    game.move_main_hero(event.pos)
                elif event.button == pg.BUTTON_RIGHT:
                    game.current_level.current_room.test_func_set_bomb(event.pos)
                elif event.button in (pg.BUTTON_WHEELUP, pg.BUTTON_WHEELDOWN):
                    game.current_level.current_room.test_func_set_pickable(event.pos)

            elif event.type == consts.MOVE_TO_NEXT_ROOM:
                game.move_to_next_room(event.direction)
            elif event.type == consts.MOVE_TO_NEXT_LEVEL:
                game.move_to_next_level()

        delta_t = timer.tick(consts.FPS) / 1000
        screen.fill(background)
        game.update(delta_t)
        game.render(screen)
        font.place_text(screen, "hello world", (300, 100))
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
