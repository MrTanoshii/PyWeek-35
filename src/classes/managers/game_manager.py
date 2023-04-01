import arcade


class GameManager(object):
    """Base class for the game manager.
    Singleton."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:  # :=
            cls.instance = super(GameManager, cls).__new__(cls)  # :=
        return cls.instance  # :=

    def __init__(self, game_window=None):
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

        self.barks: arcade.SpriteList = arcade.SpriteList()
        self.guards = arcade.SpriteList()
        self.walls: arcade.SpriteList = arcade.SpriteList()

        self.camera = None
        self.world = None

        self.game_over = False
        self.time = 0
        self.keyboard = None

        self.lights = arcade.SpriteList()

        self.player_in_light = False

        self.music_manager = None

    def set_player(self, player):
        self.player = player

    def get_guards(self):
        return self.guards

    def save_game_view(self, game_view):
        self.game_view = game_view

    def get_game_view(self):
        return self.game_view
