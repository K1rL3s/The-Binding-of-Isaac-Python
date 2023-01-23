import pygame as pg

from src.consts import STATS_WIDTH, STATS_HEIGHT, MINIMAP_WIDTH
from src.modules.Banners.UpheavalFont import UpheavalFont
from src.utils.funcs import cut_sheet, crop


class Player:
    red_hp = 9
    blue_hp = 9
    black_hp = 9
    max_red_hp = 12
    count_money = 12
    count_keys = 34
    count_bombs = 56


class HeroStats:
    size = 48
    size_s = 32
    hud = {name: crop(image) for name, image in zip(
            ("empty", "red", "blue", "black", "red_half", "blue_half", "black_half", "coin", "bomb", "key"),
            cut_sheet("textures/menu/hud.png", 4, 4, 10)
        )
    }

    """
    Отображение статов гг (хп, бомбы, монеты).

    :param main_hero: Главный герой.
    """

    def __init__(self,
                 main_hero: Player | None):
        self.main_hero = Player()  # ЗАГЛУШКА

        self.font = UpheavalFont(scale_sizes=(HeroStats.size_s, HeroStats.size_s))
        self.hearts_surface = pg.Surface((0, 0), pg.SRCALPHA, 32)
        self.other_surface = pg.Surface((0, 0), pg.SRCALPHA, 32)

        self.draw_hearts()
        self.draw_other()

    def update(self):
        self.draw_other()
        self.draw_hearts()

    def draw_hearts(self):
        self.hearts_surface = pg.Surface((HeroStats.size * 10, HeroStats.size * 2), pg.SRCALPHA, 32)
        red_hp, max_hp, blue_hp, black_hp =\
            self.main_hero.red_hp, self.main_hero.max_red_hp, self.main_hero.blue_hp, self.main_hero.black_hp,
        x, y = 0, 0
        empty_hp = max_hp - red_hp - (max_hp - red_hp) % 2

        while red_hp > 1:
            red_hp -= 2
            self.hearts_surface.blit(HeroStats.hud["red"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size
        if red_hp:
            red_hp -= 1
            self.hearts_surface.blit(HeroStats.hud["red_half"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size

        if empty_hp:
            empty_hp -= 2
            self.hearts_surface.blit(HeroStats.hud["empty"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size

        while blue_hp > 1:
            blue_hp -= 2
            self.hearts_surface.blit(HeroStats.hud["blue"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size
        if blue_hp:
            blue_hp -= 1
            self.hearts_surface.blit(HeroStats.hud["blue_half"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size

        while black_hp > 1:
            black_hp -= 2
            self.hearts_surface.blit(HeroStats.hud["black"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size
        if black_hp:
            black_hp -= 1
            self.hearts_surface.blit(HeroStats.hud["black_half"], (x, y))
            x += HeroStats.size
            if x >= HeroStats.size * 10:
                x = 0
                y += HeroStats.size

    def draw_other(self):
        self.other_surface = pg.Surface((HeroStats.size_s * 4, HeroStats.size_s * 3), pg.SRCALPHA, 32)
        self.other_surface.blit(HeroStats.hud["coin"], (0, 0))
        self.other_surface.blit(HeroStats.hud["bomb"], (0, HeroStats.size_s))
        self.other_surface.blit(HeroStats.hud["key"], (0, HeroStats.size_s * 2))

        self.font.place_text(self.other_surface, str(self.main_hero.count_money), (0, 0),
                             (HeroStats.size_s * 2, 0))
        self.font.place_text(self.other_surface, str(self.main_hero.count_bombs), (0, 0),
                             (HeroStats.size_s * 2, HeroStats.size_s))
        self.font.place_text(self.other_surface, str(self.main_hero.count_keys), (0, 0),
                             (HeroStats.size_s * 2, HeroStats.size_s * 2))

    def render(self, screen: pg.Surface):
        screen.blit(self.other_surface, (
            MINIMAP_WIDTH + HeroStats.size_s * 3, (STATS_HEIGHT - self.other_surface.get_height()) // 2
        ))
        screen.blit(self.hearts_surface, (
            STATS_WIDTH - self.hearts_surface.get_width() - HeroStats.size * 2,
            (STATS_HEIGHT - self.hearts_surface.get_height()) // 2
        ))
