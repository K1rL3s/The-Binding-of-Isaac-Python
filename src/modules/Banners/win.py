import pygame as pg

from src.consts import WIDTH, HEIGHT
from src.modules.Banners.ShopFont import ShopFont
from src.modules.mainmenu.startscrean import MenuSprite, terminate
from src.utils.funcs import load_image, add_db


def win(screen, score):
    win_list = pg.sprite.Group()
    MenuSprite(load_image(f"images/menu/win.jpg", -1), 0, 0, WIDTH, HEIGHT, win_list)
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(200)
    font = ShopFont(is_green=True)
    banner = font.write_text(f'{abs(score)}')
    screen.blit(surf, (0, 0))
    win_list.draw(screen)
    screen.blit(banner, (280, 330))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                add_db('w', score)
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    add_db('w', score)
                    terminate()
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    add_db('w', score)
                    return True
