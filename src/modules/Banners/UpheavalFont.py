from src.modules.Banners.BaseFont import BaseFont


class UpheavalFont(BaseFont):
    def __init__(self):
        BaseFont.__init__(self, "fonts/upheaval.png", "abcdefghijklmnopqrstuvwxyz0123456789$%€=?+-_ ", 26, 2, total=45)
