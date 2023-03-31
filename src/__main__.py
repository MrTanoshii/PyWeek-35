import arcade


from src.classes.managers.interactables_manager import InteractablesManager
from src.classes.windows.game import GameWindow
from pyglet.image import load as pyglet_load
from .constants import CONSTANTS as C


def main():
    InteractablesManager()
    game_window = GameWindow(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    game_window.setup()
    game_window.set_icon(pyglet_load("src/assets/icons/kiisu.png"))

    arcade.run()
