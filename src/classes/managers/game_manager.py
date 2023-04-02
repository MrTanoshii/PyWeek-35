import arcade
import math

from src.classes.story_manager import StoryManager


class GameManager(object):
    """Base class for the game manager.
    Singleton."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:  # :=
            cls.instance = super(GameManager, cls).__new__(cls)  # :=
        return cls.instance  # :=

    def __init__(self, story_manager, game_window=None, player_safes=set()):
        """
        Constructor.

        Keyword Arguments:
            game_window (GameWindow): The game window.
        """
        self.game_window = game_window
        self.game_view = None
        self.player = None
        self.collision = None
        self.score = 0
        self.story_manager = story_manager

        self.guards = arcade.SpriteList()
        self.walls: arcade.SpriteList = arcade.SpriteList()

        self.camera = None
        self.world = None

        self.game_over = False
        self.time = 0
        self.keyboard = None

        self.lights = arcade.SpriteList()
        self.light_switches = arcade.SpriteList()
        self.safes = arcade.SpriteList()
        self.total_safes_in_level = 0

        self.player_in_light = False

        self.music_manager = None
        self.player_safes = player_safes.copy()
        self.is_caught_by_guard = False
        self.hud = None

    def set_player(self, player):
        self.player = player

    def get_guards(self):
        return self.guards

    def save_game_view(self, game_view):
        self.game_view = game_view

    def get_game_view(self):
        return self.game_view

    def calculate_score(self):
        """Calculate the score."""

        self.score = 1000 * len(self.player_safes)

        decay = self.log_decline(self.time)
        self.score = self.score * decay

        if self.is_caught_by_guard:
            self.score *= 0.67

        self.score = int(self.score)

    def log_decline(self, number):
        # check if the number is between 1 and 3600
        if number < 1 or number > 3500:
            return 0.01
        # calculate the logarithmic decline using the formula y = -log(x/3600)/log(10)
        else:
            y = -math.log(number / 3600) / math.log(10)
            # return the result rounded to two decimal places
            return round(y, 2)
