class GameManager(object):
    """
    Base class for the game manager.
    Singleton.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(GameManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, game_window):
        """
        Constructor.

        Keyword Arguments:
            game_window (GameWindow): The game window.
        """

        self.game_window = game_window
        self.game_view = None
        self.player = None
        self.score = 0

    def set_player(self, player):
        self.player = player

    def save_game_view(self, game_view):
        self.game_view = game_view
    
    def get_game_view(self):
        return self.game_view
