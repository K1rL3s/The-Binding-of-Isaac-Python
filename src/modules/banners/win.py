import pygame as pg

from src.consts import HEIGHT, WIDTH
from src.modules.banners.shop_font import ShopFont
from src.modules.main_menu.start_screen import MenuSprite, terminate
from src.utils.funcs import add_db, load_image


def win(screen, score):
    win_list = pg.sprite.Group()
    MenuSprite(load_image("images/menu/win.jpg", -1), 0, 0, WIDTH, HEIGHT, win_list)
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(200)
    font = ShopFont(is_green=True)
    banner = font.write_text(f"{abs(score)}")
    screen.blit(surf, (0, 0))
    win_list.draw(screen)
    screen.blit(banner, (280, 330))
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                add_db("w", score)
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    add_db("w", score)
                    terminate()
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    add_db("w", score)
                    return True
