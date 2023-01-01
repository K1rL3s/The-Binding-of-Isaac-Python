import pygame as pg

from src import consts
from src.utils.funcs import pixels_to_cell, cell_to_pixels


pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((consts.WIDTH, consts.HEIGHT))


from src.modules.Game import Game
from src.consts import Moves
LEFT, RIGHT, UP, DOWN = Moves['LEFT'].value, Moves['RIGHT'].value, Moves['UP'].value, Moves['DOWN'].value
# фишка в том, что когда сделаем меню, можно будет позволить игроку менять настройки управления, а в коде поменяются:
settings_body = (pg.K_a, pg.K_d, pg.K_w, pg.K_s) # это
settings_head = (pg.K_KP_4, pg.K_KP_6, pg.K_KP_8, pg.K_KP_5) # и это
directions_body = {settings_body[0]: (*LEFT, "LEFT"),
                   settings_body[1]: (*RIGHT, "RIGHT"),
                   settings_body[2]: (*UP, "UP"),
                   settings_body[3]: (*DOWN, "DOWN")}

directions_head = {settings_head[0]: "LEFT",
                   settings_head[1]: "RIGHT",
                   settings_head[2]: "UP",
                   settings_head[3]: "DOWN"}
###


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
                if event.key in settings_body:
                    direction = directions_body[event.key]
                    game.main_hero.step_out_body(*direction)
                if event.key in settings_head:
                    game.main_hero.rotation_head(directions_head[event.key])
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
                if event.button == pg.BUTTON_LEFT:
                    game.move_main_hero(event.pos)
                elif event.button == pg.BUTTON_RIGHT:
                    game.current_level.current_room.test_func_set_bomb(event.pos)

        delta_t = timer.tick(consts.FPS) / 1000
        screen.fill(background)
        game.update(delta_t)
        game.render(screen)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
