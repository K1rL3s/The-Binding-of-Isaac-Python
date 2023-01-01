import pygame as pg
from src.utils.funcs import load_image
from src.consts import CELL_SIZE
# специально разбил, чтобы можно было создавать множество персонажей(понятно будет в следующих коммитах)
body_images_dict: dict = {"DOWN": [load_image(f'textures/heroes/body/forward/{i}.png') for i in range(10)],
                          "LEFT": [load_image(f'textures/heroes/body/left/{i}.png') for i in range(10)],
                          "RIGHT": [load_image(f'textures/heroes/body/right/{i}.png') for i in range(10)],
                          "UP": [load_image(f'textures/heroes/body/up/{i}.png') for i in range(10)]}

head_images_dict: dict = {"DOWN": load_image('textures/heroes/head/forward.png'),
                          "LEFT": load_image('textures/heroes/head/left.png'),
                          "RIGHT": load_image('textures/heroes/head/right.png'),
                          "UP": load_image('textures/heroes/head/up.png')}


#
class Body(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = body_images_dict["DOWN"][0]
        self.settings()

    def settings(self):
        self.indexes = {"DOWN": 0, "LEFT": 0, "RIGHT": 0, "UP": 0}

    # подумаю, как вынести в файл Animation.py
    def animating(self, name: str):
        peremennaya = self.indexes[name] + 1

        self.settings()
        self.indexes[name] = peremennaya % len(body_images_dict["DOWN"])
        self.image = body_images_dict[name][self.indexes[name]]


class Head(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = head_images_dict["DOWN"]

    # подумаю, как вынести в файл Animation.py
    def animating(self, direction: str):
        self.image = head_images_dict[direction]


# по факту - это родительский класс для песронажей( ГГ )
class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.body = Body()
        self.head = Head()
        self.image = self.get_surf_gg()
        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x + 10, CELL_SIZE * pos_y + 5)

    def update(self):
        self.image = self.get_surf_gg()

    def get_surf_gg(self) -> pg.Surface:
        surf = pg.Surface((50, 50), pg.SRCALPHA, 32)
        surf = surf.convert_alpha()
        size = self.body.image.get_size()
        coords = (25 - size[0] // 2, 52 - size[1])
        surf.blit(self.body.image, coords)
        size = self.head.image.get_size()
        surf.blit(self.head.image, (25 - size[0] // 2, coords[1] - size[1] + 13))
        return surf

    # перемещение (надо будет добавить скорость и умножать на dx/dy
    def step_out_body(self, dx, dy, name_direction):
        self.rect.x += dx
        self.rect.y += dy
        self.body.animating(name_direction)

    # поворот головы
    def rotation_head(self, name_direction):
        self.head.animating(name_direction)
###