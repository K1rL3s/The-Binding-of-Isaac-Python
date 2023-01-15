import sys
import pygame
import src.consts
import pygame as pg

from src.utils.funcs import load_image

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, img: pg.Surface, x: int, y: int, rx: int, ry: int, *group):
        super().__init__(*group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (rx, ry))

    def update(self, y):
        self.rect.y = y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('images/menu/fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    head_sprites = pygame.sprite.Group()
    anim_sprite1 = pygame.sprite.Group()
    anim_sprite2 = pygame.sprite.Group()
    MenuSprite(load_image("images/menu/head.png", -1), 100, 100, 1100, 200, head_sprites)
    MenuSprite(load_image("images/menu/isaac1.png", -1), 365, 300, 500, 500, anim_sprite1)
    MenuSprite(load_image("images/menu/isaac2.png", -1), 365, 300, 500, 500, anim_sprite2)
    dx = 90
    vy = 0.5
    i = 0
    di = 0.25
    f = 'anim_sprite1.draw(screen)'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.key != pygame.K_ESCAPE:
                    return choise_menu(screen)
                else:
                    terminate()
        screen.blit(pygame.transform.scale(load_image('images/menu/fon.png'), (WIDTH, HEIGHT)), (0, 0))
        clock.tick(40)
        head_sprites.draw(screen)
        head_sprites.update(dx)
        if i in [0, 4]:
            f = 'anim_sprite1.draw(screen)'
        elif i in [2, 6]:
            f = 'anim_sprite2.draw(screen)'
        eval(f)
        if dx == 120:
            vy = -0.5
        elif dx == 90:
            vy = 0.5
        dx += vy
        if i == 6:
            i %= 6
        i += di
        pygame.display.flip()


def create_sprite(lst: list, hero_choise_sprites: pygame.sprite.Group):
    MenuSprite(load_image(lst[0], -1), 610, 450, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(lst[1], -1), 510, 360, 80, 90, hero_choise_sprites)
    MenuSprite(load_image(lst[2], -1), 710, 360, 80, 90, hero_choise_sprites)


def draw_name(i: int):
    if i % 3 == 0:
        return f'isaac.draw(screen)'
    elif i % 3 == 1:
        return f'cain.draw(screen)'
    elif i % 3 == 2:
        return f'lost.draw(screen)'


def draw_menu(i: int):
    if i % 3 == 0:
        return f'new.draw(screen)'
    elif i % 3 == 1:
        return f'con.draw(screen)'
    elif i % 3 == 2:
        return f'opt.draw(screen)'


def return_cheack(j: int, i: int):
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
    fon = pygame.transform.scale(load_image('images/menu/choise_fon.png'), (WIDTH, HEIGHT))
    whoam = pygame.sprite.Group()
    list_hero = ["images/menu/isaac.png", "images/menu/cain.png", "images/menu/lost.png"]
    MenuSprite(load_image("images/menu/whoam.png", -1), 350, 100, 600, 740, whoam)
    MenuSprite(load_image("images/menu/left.png", -1), 510, 560, 50, 50, whoam)
    MenuSprite(load_image("images/menu/right.png", -1), 710, 560, 50, 50, whoam)
    MenuSprite(load_image("images/menu/sheet.png", -1), 880, 200, 700, 600, whoam)

    MenuSprite(load_image("images/menu/new_run.png", -1), 945, 300, 280, 90, whoam)
    MenuSprite(load_image("images/menu/continue_true.png", -1), 950, 370, 280, 90, whoam)
    MenuSprite(load_image("images/menu/options.png", -1), 955, 435, 280, 90, whoam)

    MenuSprite(load_image("images/menu/right.png", -1), 905, 335, 50, 50, new := pygame.sprite.Group())
    MenuSprite(load_image("images/menu/right.png", -1), 910, 405, 50, 50, con := pygame.sprite.Group())
    MenuSprite(load_image("images/menu/right.png", -1), 910, 475, 50, 50, opt := pygame.sprite.Group())

    MenuSprite(load_image("images/menu/isaac_name.png", -1), 570, 550, 150, 70, isaac := pygame.sprite.Group())
    MenuSprite(load_image("images/menu/cain_name.png", -1), 570, 550, 150, 70, cain := pygame.sprite.Group())
    MenuSprite(load_image("images/menu/lost_name.png", -1), 560, 540, 160, 90, lost := pygame.sprite.Group())
    MenuSprite(load_image("images/menu/isaac_info.png", -1), 480, 630, 350, 70, isaac)
    MenuSprite(load_image("images/menu/lost_info.png", -1), 480, 630, 350, 70, lost)
    MenuSprite(load_image("images/menu/cain_info.png", -1), 480, 630, 350, 70, cain)
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
                terminate()
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
                    return 0
                elif event.key == pygame.K_ESCAPE:
                    return start_screen(screen)
            whoam.draw(screen)
            hero_choise_sprites.draw(screen)
            eval(f)
            eval(f1)
            pygame.display.flip()
