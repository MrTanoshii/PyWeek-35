import os
import arcade
from random import randint

from src.classes.managers.game_manager import GameManager
from src.constants import CONSTANTS as C


class ExitSprite(arcade.Sprite):

    servers = arcade.SpriteList()

    """server light"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_path = "src/assets/art/exit.png"
        self.texture = arcade.load_texture(base_path)
        self.scale = 0.25

    def draw(self):
        super().draw()
