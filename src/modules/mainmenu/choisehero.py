import pygame
from src.modules.mainmenu.startscrean import start_screen
from src.modules.mainmenu.startscrean import MenuSprite
import src.consts
from src.utils.funcs import load_image

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def create_sprite(lst, hero_choise_sprites):
    MenuSprite(load_image(lst[0], -1), 610, 450, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(lst[1], -1), 510, 360, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(lst[2], -1), 710, 360, 80, 90, hero_choise_sprites)


def draw_name(i):
    if i % 3 == 0:
        return f'isaac.draw(screen)'
    elif i % 3 == 1:
        return f'cain.draw(screen)'
    elif i % 3 == 2:
        return f'lost.draw(screen)'


def draw_menu(i):
    if i % 3 == 0:
        return f'new.draw(screen)'
    elif i % 3 == 1:
        return f'con.draw(screen)'
    elif i % 3 == 2:
        return f'opt.draw(screen)'


def return_cheack(j, i):
    if j % 3 == 0:
        if i % 3 == 0:
            return f'isaac'
        elif i % 3 == 1:
            return f'cain'
        elif i % 3 == 2:
            return f'lost'
    elif j % 3 == 1:
        return None
        # допилить Меню
    elif j % 3 == 2:
        return None


# Возвращает имя персонажа (допилить возврат управления)
def choise_menu(screen):
    fon = pygame.transform.scale(load_image('choise_fon.png'), (WIDTH, HEIGHT))
    whoam = pygame.sprite.Group()
    list_hero = ["isaac.png", "cain.png", "lost.png"]
    MenuSprite(load_image("whoam.png", -1), 350, 100, 600, 740, whoam)
    MenuSprite(load_image("left.png", -1), 510, 560, 50, 50, whoam)
    MenuSprite(load_image("right.png", -1), 710, 560, 50, 50, whoam)
    MenuSprite(load_image("sheet.png", -1), 880, 200, 700, 600, whoam)

    MenuSprite(load_image("new_run.png", -1), 945, 300, 280, 90, whoam)
    MenuSprite(load_image("continue_true.png", -1), 950, 370, 280, 90, whoam)
    MenuSprite(load_image("options.png", -1), 955, 435, 280, 90, whoam)

    MenuSprite(load_image("right.png", -1), 905, 335, 50, 50, new := pygame.sprite.Group())
    MenuSprite(load_image("right.png", -1), 910, 405, 50, 50, con := pygame.sprite.Group())
    MenuSprite(load_image("right.png", -1), 910, 475, 50, 50, opt := pygame.sprite.Group())

    MenuSprite(load_image("isaac_name.png", -1), 570, 550, 150, 70, isaac := pygame.sprite.Group())
    MenuSprite(load_image("cain_name.png", -1), 570, 550, 150, 70, cain := pygame.sprite.Group())
    MenuSprite(load_image("lost_name.png", -1), 560, 540, 160, 90, lost := pygame.sprite.Group())
    MenuSprite(load_image("isaac_info.png", -1), 480, 630, 350, 70, isaac)
    MenuSprite(load_image("lost_info.png", -1), 480, 630, 350, 70, lost)
    MenuSprite(load_image("cain_info.png", -1), 480, 630, 350, 70, cain)

    screen.blit(fon, (0, 0))
    hero_choise_sprites = pygame.sprite.Group()
    MenuSprite(load_image(list_hero[0], -1), 610, 450, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(list_hero[1], -1), 510, 360, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(list_hero[2], -1), 710, 360, 80, 90, hero_choise_sprites)
    i = 0
    j = 0
    f = f'isaac.draw(screen)'
    f1 = f'new.draw(screen)'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    i += 1
                    hero_choise_sprites = pygame.sprite.Group()
                    whoam.draw(screen)
                    f = draw_name(i)
                    list_hero = list_hero[1:] + list_hero[:1]
                    create_sprite(list_hero, hero_choise_sprites)
                    hero_choise_sprites.draw(screen)
                elif event.key == pygame.K_RIGHT:
                    i -= 1
                    hero_choise_sprites = pygame.sprite.Group()
                    whoam.draw(screen)
                    f = draw_name(i)
                    list_hero = list_hero[-1:] + list_hero[:-1]
                    create_sprite(list_hero, hero_choise_sprites)
                    hero_choise_sprites.draw(screen)
                elif event.key == pygame.K_DOWN:
                    j += 1
                    f1 = draw_menu(j)
                elif event.key == pygame.K_UP:
                    j -= 1
                    f1 = draw_menu(j)
                elif event.key == pygame.K_RETURN:
                    if return_cheack(j, i) is not None:
                        return return_cheack(j, i)
                elif event.key == pygame.K_ESCAPE:
                    return start_screen(screen)

            whoam.draw(screen)
            hero_choise_sprites.draw(screen)
            eval(f)
            eval(f1)
            pygame.display.flip()
