import arcade


class Wall(arcade.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(":resources:images/tiles/stoneMid.png")
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
