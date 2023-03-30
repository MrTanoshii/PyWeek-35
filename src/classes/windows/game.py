import arcade

from src.constants import CONSTANTS as C
from src.classes.managers.game_manager import GameManager
from src.classes.views.game_view import GameView
from src.classes.views.ingame_menu_view import IngameMenuView
from src.classes.views.score_view import ScoreView
from src.classes.entities.player import Player


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # create a player list, and a player (None for now, they will come in setup)
        self.player = None
        # makes a dictionary of A-Z0-9LEFTRIGHTDOWNUP:0. will be used to read keypresses by player
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
        # Setup views
        self.game_view = GameView()
        self.ingame_menu_view = IngameMenuView()
        # TODO: Might need to move this somewhere else and trigger it accordingly
        self.score_view = ScoreView(self.game_view)

        # Let's add the player, and add them to the playerlist
        self.player = Player(keyboard=self.keyboard, game_manager=game_manager)
        coords = game_manager.world.player_spawn[0].coordinates
        self.player.scale = 1
        self.player.center_x = coords.x * C.WORLD_SCALE
        self.player.center_y = (C.SCREEN_HEIGHT - coords.y - 96) * C.WORLD_SCALE
        game_manager.set_player(self.player)

        # Set the initial view
        self.show_view(self.game_view)

    def on_update(self, delta_time: float):
        self.player.on_update(delta_time=delta_time)
        print(len(self.game_manager.walls))
        return super().on_update(delta_time)

    def on_draw(self):
        self.player.draw()
        return super().on_draw()

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
        # TODO REMOVE FOR RELEASE
        elif key == arcade.key.ESCAPE:
            arcade.exit()

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
        # Set the initial view
        self.show_view(self.game_view)
