import pygame as pg

from src.utils.funcs import load_image
from src.consts import GAME_WIDTH, GAME_HEIGHT, WALL_SIZE


class HpBossBar(pg.sprite.Sprite):
    img = load_image("images/menu/hpbar.png")

    def __init__(self, hp: int, *group):
        super().__init__(*group)
        self.image = HpBossBar.img
        self.rect = self.image.get_rect()
        self.hp_max = hp
        self.hp = hp
        self.rect.center = (GAME_WIDTH // 2, GAME_HEIGHT - WALL_SIZE)
        self.image = pg.transform.scale(self.image, (450, 96))
        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH // 2, GAME_HEIGHT - WALL_SIZE // 2)

    def hurt(self, damage: int):
        self.hp = max(self.hp - damage, 0)
        self.image = self.image.subsurface(0, 0, self.hp / self.hp_max * 450, 96)


class HpBossBarRam(pg.sprite.Sprite):
    img = load_image("images/menu/hpbarram.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = HpBossBarRam.img
        self.image = pg.transform.scale(self.image, (450, 96))
        self.rect = self.image.get_rect()
        self.rect.center = (GAME_WIDTH // 2, GAME_HEIGHT - WALL_SIZE // 2)
