import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)
WIDTH, HEIGHT = 1280, 960
STEP = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None, musik=False):
    fullname = os.path.join("src\data\images\menu", name)
    if musik:
        return os.path.join("src\data\sounds", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class MenuSprite(pygame.sprite.Sprite):
    image = load_image("head.png", -1)

    def __init__(self, img, x, y, rx, ry, *group):
        super().__init__(*group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (rx, ry))

    def update(self, y):
        self.rect.y = y


def start_screen():
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    head_sprites = pygame.sprite.Group()
    anim_sprite1 = pygame.sprite.Group()
    anim_sprite2 = pygame.sprite.Group()
    MenuSprite(load_image("head.png", -1), 100, 100, 1100, 200, head_sprites)
    MenuSprite(load_image("isaac1.png", -1), 365, 300, 500, 500, anim_sprite1)
    MenuSprite(load_image("isaac2.png", -1), 365, 300, 500, 500, anim_sprite2)
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
                return 0
        screen.blit(pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT)), (0, 0))
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
