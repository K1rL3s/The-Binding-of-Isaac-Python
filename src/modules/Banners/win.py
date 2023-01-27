import sys

import pygame
import src.consts
import pygame as pg
import random

from src.modules.Banners.ShopFont import ShopFont
from src.modules.mainmenu import startscrean

from src.modules.mainmenu.startscrean import MenuSprite, terminate
from src.utils.funcs import load_image, add_db

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def win(screen, score=1000):
    win_list = pygame.sprite.Group()
    MenuSprite(load_image(f"images/menu/win.jpg", -1), 0, 0, WIDTH, HEIGHT, win_list)
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(200)
    font = ShopFont(green=True)
    banner = font.write_text(f'{abs(score)}')
    screen.blit(surf, (0, 0))
    win_list.draw(screen)
    screen.blit(banner, (280, 330))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    add_db('w', score)
                    terminate()
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    add_db('w', score)
                    return True
