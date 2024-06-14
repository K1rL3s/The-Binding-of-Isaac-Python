from src.modules.banners.base_font import BaseFont


class ShopFont(BaseFont):
    def __init__(self, is_black: bool = False, is_green: bool = False):
        image = "fonts/prices"
        if is_black:
            image += "_black"
        elif is_green:
            image += "green"
        BaseFont.__init__(self, f"{image}.png", "0123456789c$", 12, 1, total=12)
