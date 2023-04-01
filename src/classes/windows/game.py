import arcade

from src.constants import CONSTANTS as C
from src.classes.managers.game_manager import GameManager
from src.classes.views.game_view import GameView
from src.classes.views.ingame_menu_view import IngameMenuView
from src.classes.views.score_view import ScoreView

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # makes a dictionary of A-Z0-9LEFTRIGHTDOWNUP:0. will be used to read keypresses by user
        self.keyboard = {
            x: 0
            for x in [chr(y) for y in range(65, 91)] + [chr(z) for z in range(48, 58)] + ["LEFT", "RIGHT", "DOWN", "UP"]
        }
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        self.game_manager = None

    def setup(self):
        # Set up the game manager
        game_manager = GameManager(self)
        self.game_manager = game_manager
        self.game_manager.keyboard = self.keyboard
        # Setup views
        self.game_view = GameView()
        self.ingame_menu_view = IngameMenuView(self.game_view)
        # TODO: Might need to move this somewhere else and trigger it accordingly
        self.score_view = None


        # Set the initial view
        self.show_view(self.game_view)

    def on_update(self, delta_time: float):
        if GameManager.instance.game_over:
            if self.score_view is None:
                self.score_view = ScoreView(self.game_view)
            if self.game_manager is not None:
                self.game_manager.lights.clear()
                self.game_manager.walls.clear()
                self.game_view = None
                del(self.game_manager.player)
                self.game_manager = None

            self.show_view(self.score_view)
        else:
            pass
        return super().on_update(delta_time)

    def on_key_press(self, key, modifiers):
        """called whenever a key is pressed"""

        if key == arcade.key.W:
            self.keyboard["W"] = 1
        elif key == arcade.key.S:
            self.keyboard["S"] = 1
        elif key == arcade.key.A:
            self.keyboard["A"] = 1
        elif key == arcade.key.D:
            self.keyboard["D"] = 1
        elif key == arcade.key.LEFT:
            self.keyboard["LEFT"] = 1
        elif key == arcade.key.RIGHT:
            self.keyboard["RIGHT"] = 1
        elif key == arcade.key.UP:
            self.keyboard["UP"] = 1
        elif key == arcade.key.DOWN:
            self.keyboard["DOWN"] = 1

    def on_key_release(self, key, modifiers):
        """called whenever the user releases a key"""
        if key == arcade.key.W:
            self.keyboard["W"] = 0
        elif key == arcade.key.S:
            self.keyboard["S"] = 0
        elif key == arcade.key.A:
            self.keyboard["A"] = 0
        elif key == arcade.key.D:
            self.keyboard["D"] = 0
        elif key == arcade.key.LEFT:
            self.keyboard["LEFT"] = 0
        elif key == arcade.key.RIGHT:
            self.keyboard["RIGHT"] = 0
        elif key == arcade.key.UP:
            self.keyboard["UP"] = 0
        elif key == arcade.key.DOWN:
            self.keyboard["DOWN"] = 0
        elif key == arcade.key.ESCAPE:
            self.show_view(self.ingame_menu_view)