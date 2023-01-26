# import random

import pygame as pg

# from src.consts import USE_BOMB, MOVE_TO_NEXT_ROOM, Moves
from src.consts import USE_BOMB, HeartsTypes
from src.modules.characters.parents import Player
from src.modules.entities.items import PickMoney, PickHeart, PickBomb, PickKey
# from src.modules.entities.artifacts import (Dinner, FreshMeat, GreySyringe, GreenSyringe, MomsHeels, PurpleSyringe,
#                                             RedSyringe, WhiteSyringe)


class MainHeroActionsHandler:
    """
    Обработчик событий для главного героя.
    В данный момент - временный. Ростик, переделай под себя.
    """

    def __init__(self, main_hero: Player):
        self.main_hero = main_hero

    def keyboard_handler(self, event: pg.event.Event):
        """
        Обработчик нажатий на клавиатуру.

        :param event: Ивент нажатия или отпуская кнопки.
        """
        is_down = event.type == pg.KEYDOWN
        # if is_valid is True:
        #     return True
        # else:
        #     return False
        self.main_hero.set_flags_move(event, is_down)

        if event.key == pg.K_e:
            if self.main_hero.get_count_bombs():
                pg.event.post(pg.event.Event(USE_BOMB, {"pos": self.main_hero.rect.center}))

    def loot_pickup_handler(self, event: pg.event.Event):
        """
        Обработка подбора лута.

        :param event: Ивент, который содержит item (PickableItem), count (int) и self (вызывается PickableItem).
        """
        name_loot = event.item.__class__
        if name_loot == PickMoney:
            self.main_hero.count_money += event.item.count
            event.item.kill()
        elif name_loot == PickHeart:
            if self.main_hero.pickup_heart(event.count, event.heart_type):
                event.item.kill()
        elif name_loot == PickBomb:
            self.main_hero.count_bombs += event.item.count
            event.item.kill()
        elif name_loot == PickKey:
            self.main_hero.count_key += event.item.count
            event.item.kill()

    def artifact_pickup_handler(self, event: pg.event.Event):
        """
        Обработка подбора артефакта.

        :param event: Ивент, который содержит item (BaseArtifact) и self (Pedestal) (вызывается Pedestal).
        """
        boosts: dict[str, int] = event.item.__class__.boosts
        if "max_hp" in boosts.keys():
            self.main_hero.max_red_hp += boosts["max_hp"] * 2
        if "heal_hp" in boosts.keys():
            self.main_hero.pickup_heart(boosts['heal_hp'] * 2, HeartsTypes.RED)
        if "damage" in boosts.keys():
            self.main_hero.head.shot_damage += boosts['damage']
        if "speed" in boosts.keys():
            self.main_hero.max_speed += boosts['speed']
        if "shot_speed" in boosts.keys():
            self.main_hero.head.shot_speed += boosts['shot_speed']
        if "shot_distance" in boosts.keys():
            self.main_hero.head.shot_max_distance += boosts["shot_distance"]
        if "shot_delay" in boosts.keys():
            self.main_hero.head.shot_delay += boosts["shot_delay"]
        event.item.kill()

    def buy_handler(self, event: pg.event.Event):
        """
        обработка покупки предмета.

        :param event: Ивент, который содержит item (PickableItem), count (int), price (int), self (ShopItem)
                      и иногда heart_type (HeartsTypes).
        """
        if self.main_hero.is_buy(event.count, event.price, event.heart_type):
            if not event.heart_type:
                self.loot_pickup_handler(event)
            event.item.kill()
            event.self.kill()
