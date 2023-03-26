import arcade

from constants import CONSTANTS as C
from classes.managers.game_manager import GameManager
from classes.views.game_view import GameView
from classes.views.ingame_menu_view import IngameMenuView


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def setup(self):
        # Setup the game manager
        GameManager()

        # Setup views
        self.game_view = GameView()
        self.ingame_menu_view = IngameMenuView()

        # Set the initial view
        self.show_view(self.game_view)

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass
