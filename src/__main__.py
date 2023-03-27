import arcade

from constants import CONSTANTS as C
from classes.managers.game_manager import GameManager
from classes.managers.interactables_manager import InteractablesManager
from classes.windows.game import GameWindow


if __name__ == "__main__":
    # Setup managers
    InteractablesManager()

    game_window = GameWindow(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE)
    game_window.setup()

    # Setup game manager
    GameManager(game_window)

    arcade.run()
