import arcade


class GameManager(object):
    """Base class for the game manager.
    Singleton."""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, game_window=None):
        self.game_window = game_window
        self.player = None
        self.collision = None
        self.score = 0
        self.guards = []
        self.walls = None
        self.camera = None
        self.world = None

    def set_player(self, player):
        self.player = player
