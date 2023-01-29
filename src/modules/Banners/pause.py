import pygame
import src.consts
import pygame as pg

from src.modules.mainmenu.startscrean import MenuSprite
from src.utils.funcs import load_image

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def pause(screen, hero: str):
    pause_list = pygame.sprite.Group()
    MenuSprite(load_image(f"images/menu/pause_{hero}.png", -1), 250, 100, 800, 740, pause_list)
    surf = pg.Surface((WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    surf.set_alpha(140)
    screen.blit(surf, (0, 0))
    pause_list.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                    return
