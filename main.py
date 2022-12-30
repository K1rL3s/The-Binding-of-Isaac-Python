import pygame as pg

from src import consts


pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))


from src.modules.Game import Game


def main():
    running = True
    timer = pg.time.Clock()
    background = pg.Color(27, 24, 24)

    game = Game()

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
                    game.next_level()
            if event.type == pg.MOUSEBUTTONDOWN:
                game.move_main_hero(event.pos)

        delta_t = timer.tick(60) / 1000
        screen.fill(background)
        game.update(delta_t)
        game.render(screen)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
