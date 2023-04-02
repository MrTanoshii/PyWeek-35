import os

import arcade

from src.constants import CONSTANTS as C
from src.classes.managers.game_manager import GameManager


class HUD:
    """Class for the HUD"""

    def __init__(self):
        self.camera = arcade.Camera(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

        self.inventory = arcade.SpriteList()

        self.asset_path = f"src/assets/art/storage_devices/"

        self.text_box = None
        self.story_line = "Placeholder text"

        self.setup()

    def setup(self):
        """Set up HUD"""
        for idx, asset in enumerate(os.listdir(self.asset_path)):
            sprite = arcade.Sprite(
                f"{self.asset_path}/{asset}",
                hit_box_algorithm="Simple",
                center_y=C.SCREEN_HEIGHT - 50,
                center_x=idx * 90 + 50,
            )
            sprite.color = (5, 5, 5)
            self.inventory.append(sprite)
        # self.inventory[2].color = (255, 255, 255)

        story = GameManager.instance.story_manager
        self.story_line = story.next_story()

    def draw(self):
        """Draw the HUD"""
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

        if self.story_line:
            # Draw the text

            self.text_box = arcade.Text(
                self.story_line,
                C.SCREEN_WIDTH // 2,
                C.SCREEN_HEIGHT * 0.1 // 1,
                arcade.color.WHITE,
                font_size=30,
                multiline=True,
                width=C.SCREEN_WIDTH * 0.8,
                anchor_x="center",
                align="center",
            )

            arcade.draw_rectangle_filled(
                self.text_box.position[0],
                self.text_box.position[1] + self.text_box.y // 2 - self.text_box.content_height // 2,
                self.text_box.content_width * 1.1,
                self.text_box.content_height * 1.1,
                (0, 0, 0, 128),
            )

            self.text_box.draw()

        self.inventory.draw()

    def on_update(self, delta_time: float):
        for index, safe in enumerate(self.inventory):
            if index in GameManager.instance.player_safes:
                safe.color = (255, 255, 255)
            else:
                safe.color = (5, 5, 5)

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.SPACE or key == arcade.key.E:
            story = GameManager.instance.story_manager
            self.story_line = story.next_story()

    def set_story_line(self, story_line):
        """Set story line immediately in game loop."""
        self.story_line = story_line
