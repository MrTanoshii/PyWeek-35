class GameManager(object):
    """Base class for the game manager.
    Singleton."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.player = None
        self.score = 0

    def set_player(self, player):
        self.player = player
