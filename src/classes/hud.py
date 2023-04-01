import os

import arcade

from src.constants import CONSTANTS as C


class HUD:
    def __init__(self):
        self.camera = arcade.Camera(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

        self.inventory = arcade.SpriteList()

        self.asset_path = f"src/assets/art/storage_devices/"

        self.setup()

    def setup(self):
        for idx, asset in enumerate(os.listdir(self.asset_path)):
            sprite = arcade.Sprite(
                f"{self.asset_path}/{asset}",
                hit_box_algorithm="Simple",
                center_y=C.SCREEN_HEIGHT - 50,
                center_x=idx * 90 + 50,
            )
            sprite.color = (5, 5, 5)
            self.inventory.append(sprite)
        self.inventory[2].color = (255, 255, 255)

    def draw(self):
        self.camera.use()
        arcade.draw_rectangle_filled(
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT - 30,
            C.SCREEN_WIDTH // 4,
            60,
            (0, 0, 0, 200),
        )

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

        self.inventory.draw()
