import arcade
from src.constants import CONSTANTS as C
from random import randint


class Light(arcade.Sprite):
    """Light sprite"""

    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.light_radius = radius * 3.75
        self.enabled = True
        self.reset_time = 5
        self.timer = randint(0, 5)
        self.hit_box_algorithm = "Simple"

    def on_update(self, dt):
        # if not self.enabled:
        self.timer += dt
        if self.timer >= self.reset_time:
            self.toggle()
            self.timer = 0

    def draw(self):
        if not self.enabled:
            return
        super().draw()

        if C.DEBUG:
            # Draw border
            arcade.draw_circle_outline(
                self.center_x, self.center_y, self.light_radius, (255, 255, 0, 255)
            )

    def toggle(self):
        self.enabled = not self.enabled
