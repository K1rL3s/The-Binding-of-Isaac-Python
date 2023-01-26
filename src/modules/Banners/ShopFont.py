from src.modules.Banners.BaseFont import BaseFont


class ShopFont(BaseFont):
    def __init__(self, black=False, green=False):
        if not black and not green:
            BaseFont.__init__(self, "fonts/prices.png", "0123456789c$", 12, 1, total=12)
        else:
            if green:
                BaseFont.__init__(self, "fonts/prices_green.png", "0123456789c$", 12, 1, total=12)
            else:
                BaseFont.__init__(self, "fonts/prices_black.png", "0123456789c$", 12, 1, total=12)
