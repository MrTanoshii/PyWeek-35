import arcade

from classes.windows.game import GameWindow
from constants import CONSTANTS as C


if __name__ == "__main__":
    game_window = GameWindow(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    game_window.setup()
    arcade.run()
