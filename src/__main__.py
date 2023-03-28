import arcade

from src.classes.windows.game import GameWindow
from .constants import CONSTANTS as C


def main():
    game_window = GameWindow(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    game_window.setup()
    arcade.run()
