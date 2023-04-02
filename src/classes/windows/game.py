import arcade

from src.classes.managers.game_manager import GameManager
from src.classes.managers.music_manager import MusicManager
from src.classes.story_manager import StoryManager
from src.classes.views.game_view import GameView
from src.classes.views.ingame_menu_view import IngameMenuView
from src.classes.views.mainmenu_view import MainMenuView
from src.classes.views.score_view import ScoreView


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # makes a dictionary of A-Z0-9LEFTRIGHTDOWNUP:0. will be used to read keypresses by user
        self.ingame_menu_view = None
        self.game_view = None
        self.score_view = None
        self.keyboard = {
            x: 0
            for x in [chr(y) for y in range(65, 91)] + [chr(z) for z in range(48, 58)] + ["LEFT", "RIGHT", "DOWN", "UP"]
        }
        arcade.set_background_color(arcade.color.ARMY_GREEN)
        self.game_manager = None
        self.music_manager = MusicManager()
        self.story_manager = StoryManager()

    def setup(self, stop_outro: bool = False):
        # Set up the game manager
        game_manager = GameManager(self.story_manager, self)
        self.game_manager = game_manager
        self.game_manager.keyboard = self.keyboard
        game_manager.music_manager = self.music_manager

        # Setup views
        self.mainmenu_view = MainMenuView(self)
        self.score_view = None
        self.game_view = None
        self.ingame_menu_view = None

        # Set the initial view
        self.show_view(self.mainmenu_view)

        # Music
        self.music_manager.stop()

        self.music_manager.play_main()
        self.game_manager.music_manager = self.music_manager

    def start_level(self, level):
        self.game_view = GameView(level + 1)
        self.ingame_menu_view = IngameMenuView(self.game_view)
        self.show_view(self.game_view)

    def on_update(self, delta_time: float):
        if GameManager.instance.game_over:
            if self.score_view is None:
                self.music_manager.play_outro()
                self.score_view = ScoreView(self.game_view, self)
            self.show_view(self.score_view)

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
