import sys
import pygame
import src.consts
import pygame as pg
from src.utils.funcs import load_image


class HpBossBar(pygame.sprite.Sprite):
    img = load_image("images/menu/hpbar.png")

    def __init__(self, hp: int, *group):
        super().__init__(*group)
        self.image = HpBossBar.img
        self.rect = self.image.get_rect()
        self.hp_max = hp
        self.hp = hp
        self.rect.x = 415
        self.rect.y = 670
        self.image = pygame.transform.scale(self.image, (450, 96))

    def hurt(self, damage: int):
        self.hp -= damage
        self.image = self.image.subsurface(0, 0, self.hp / self.hp_max * 450, 96)


class HpBossBarRam(pygame.sprite.Sprite):
    img = load_image("images/menu/hpbarram.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = HpBossBarRam.img
        self.rect = self.image.get_rect()
        self.rect.x = 415
        self.rect.y = 670
        self.image = pygame.transform.scale(self.image, (450, 96))

