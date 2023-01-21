from src.modules.Banners.BaseFont import BaseFont


class ShopFont(BaseFont):
    def __init__(self):
        BaseFont.__init__(self, "fonts/prices.png", "0123456789c$", 12, 1, total=12)
