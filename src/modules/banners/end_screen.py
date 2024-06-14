import random
import sys

import pygame
import pygame as pg

import src.consts
from src.modules.banners.shop_font import ShopFont
from src.modules.main_menu.start_screen import MenuSprite
from src.utils.funcs import add_db, load_image

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def terminate():
    pygame.quit()
    sys.exit()


def end_screen(screen, hero, score):
    end_list = pygame.sprite.Group()
    MenuSprite(
        load_image("images/menu/death_list.png", -1),
        320,
        100,
        660,
        760,
        end_list,
    )
    MenuSprite(
        load_image(f"images/menu/{hero}_name.png", -1),
        780,
        223,
        150,
        70,
        name := pygame.sprite.Group(),
    )
    MenuSprite(
        load_image(f"images/menu/deth/image_part_00{random.randint(1, 9)}.png", -1),
        670,
        400,
        150,
        90,
        name,
    )
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(200)
    font = ShopFont(is_black=True)
    banner = font.write_text(f"{abs(score)}")
    screen.blit(surf, (0, 0))
    end_list.draw(screen)
    name.draw(screen)
    screen.blit(banner, (430, 610))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                add_db("l", score)
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    add_db("l", score)
                    terminate()
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    add_db("l", score)
                    return True
