import arcade

from constants import CONSTANTS as C


class HUD:
    def __int__(self):
        self.score = 0

    def draw(self):
        arcade.draw_rectangle_filled(C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT - 30, C.SCREEN_WIDTH // 4, 60, (0, 0, 0, 200))

        arcade.draw_text(
            "Files retrieved: 0/0",
            C.SCREEN_WIDTH // 2,
            C.SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            font_size=20,
            font_name="Minecraft",
            anchor_x="center",
            anchor_y="center",
        )
