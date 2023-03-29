import arcade


class Guards:
    def __init__(self):
        self.guards = []

    def append(self, guard):
        self.guards.append(guard)

    def draw(self):
        for guard in self.guards:
            guard.draw()

    def on_update(self, dt):
        for guard in self.guards:
            guard.on_update(dt)


guards = Guards()


class GameManager(object):
    """Base class for the game manager.
    Singleton."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:  # :=
            cls.instance = super(GameManager, cls).__new__(cls)  # :=
        return cls.instance  # :=

    def __init__(self, game_window=None):
        self.game_window = game_window
        self.player = None
        self.collision = None
        self.score = 0

        self.guards = guards
        self.walls: arcade.SpriteList = arcade.SpriteList()

        self.camera = None
        self.world = None

    def set_player(self, player):
        self.player = player

    def get_guards(self):
        return guards.guards
