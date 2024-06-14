from src.modules.banners.base_font import BaseFont


class UpheavalFont(BaseFont):
    def __init__(self, is_black: bool = False, scale_sizes: tuple[int, int] = None):
        image = "fonts/upheaval"
        if is_black:
            image += "_black"
        BaseFont.__init__(
            self,
            f"{image}.png",
            "abcdefghijklmnopqrstuvwxyz0123456789$%€=?+-_ ",
            26,
            2,
            total=45,
            scale_sizes=scale_sizes,
        )
