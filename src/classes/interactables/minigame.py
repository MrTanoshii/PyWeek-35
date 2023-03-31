import arcade

class MiniGame(arcade.View):
    """Base class for minigames."""
   
    def __init__(self, minigame: object):
        super().__init__()
        self.window.show_view(minigame)