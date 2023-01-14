import pygame
import pygame as pg
from src import consts
from src.utils.funcs import pixels_to_cell, cell_to_pixels


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
                game.main_hero.set_flags_move(event, True)
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
            if event.type == pg.KEYUP:
                game.main_hero.set_flags_move(event, False)
            if event.type == consts.MOVE_TO_NEXT_ROOM:
                direction = event.direction
                next_coords = event.next_coords
                game.move_main_hero(next_coords)
                game.move_to_next_room(direction)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_RIGHT:
                    game.current_level.current_room.test_func_set_bomb(event.pos)

        delta_t = timer.tick(consts.FPS) / 1000
        screen.fill(background)
        game.update(delta_t)
        game.render(screen)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
