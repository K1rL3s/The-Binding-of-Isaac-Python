import pygame as pg

from src.consts import USE_BOMB


class MainHeroActionsHandler:
    """
    Обработчик событий для главного героя.
    В данный момент - временный. Ростик, переделай под себя.
    """

    def __init__(self, main_hero: pg.sprite.Sprite):
        self.main_hero = main_hero

    def keyboard_handler(self, event: pg.event.Event):
        """
        Обработчик нажатий на клавиатуру.

        :param event: Ивент нажатия или отпуская кнопки.
        """
        if event.key == pg.K_w:
            self.main_hero.rect.move_ip(0, -10)
        elif event.key == pg.K_a:
            self.main_hero.rect.move_ip(-10, 0)
        elif event.key == pg.K_s:
            self.main_hero.rect.move_ip(0, 10)
        elif event.key == pg.K_d:
            self.main_hero.rect.move_ip(10, 0)

        # Сделать обработку кол-ва бомб!
        elif event.key == pg.K_e:
            pg.event.post(pg.event.Event(USE_BOMB, {"pos": self.main_hero.rect.center}))

        # Временно!!! (хотел сюда спавн пик-лута поставить, но ладно уже)
        elif event.key == pg.K_r:
            pg.event.post(pg.event.Event(USE_BOMB, {"pos": (self.main_hero.rect.centerx,
                                                            self.main_hero.rect.bottom - 100)}))

    def loot_pickup_handler(self, event: pg.event.Event):
        """
        Обработка подбора лута.

        :param event: Ивент, который содержит item (PickableItem), count (int) и self (вызывается PickableItem).
        """
        print(f"loot {event.item.__class__.__name__}")

    def artifact_pickup_handler(self, event: pg.event.Event):
        """
        Обработка подбора артефакта.

        :param event: Ивент, который содержит item (BaseArtifact) и self (Pedestal) (вызывается Pedestal).
        """
        print(f"art {event.item.__class__.__name__}")

    def buy_handler(self, event: pg.event.Event):
        """
        обработка покупки предмета.

        :param event: Ивент, который содержит item (PickableItem), count (int), price (int), self (ShopItem)
                      и иногда heart_type (HeartsTypes).
        """
        print(f"buy {event.item.__class__.__name__}")

