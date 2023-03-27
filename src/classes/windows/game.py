import arcade

from constants import CONSTANTS as C
from classes.managers.game_manager import GameManager
from classes.views.game_view import GameView
from classes.views.ingame_menu_view import IngameMenuView
from classes.entities.player import Player


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(C.BACKGROUND_COLOR)
        self.player_list = None
        self.player = None
        # makes a dictionary of A-Z0-9LEFTRIGHTDOWNUP:0. will be used to read keypresses by player
        self.keyboard = {x:0 for x in [chr(y) for y in range(65, 91)] + [chr(z) for z in range(48,58)] + ['LEFT', 'RIGHT', 'DOWN', 'UP']}

    def setup(self):
        # Setup the game manager
        GameManager(self)

        # Setup views
        self.game_view = GameView()
        self.ingame_menu_view = IngameMenuView()

        self.player_list = arcade.SpriteList()
        self.player = Player(filename='src\\assets\\panda\\0001.png', keyboard = self.keyboard)
        self.player.center_x = 50
        self.player.center_y = 50
        self.player_list.append(self.player)
        # Set the initial view
        self.show_view(self.game_view)

    def on_update(self, delta_time: float):
        self.player_list.update()
        return super().on_update(delta_time)
        
        
        
        
    def on_draw(self):
        self.player_list.draw()

        return super().on_draw()
    
    def on_key_press(self, key, modifiers):
        ''' called whenever a key is pressed '''
        print(key, arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D)

        if key == arcade.key.W:
            self.keyboard['W'] = 1
        elif key == arcade.key.S:
            self.keyboard['S'] = 1
        elif key == arcade.key.A:
            self.keyboard['A'] = 1
        elif key == arcade.key.D:
            self.keyboard['D'] = 1
        elif key == arcade.key.LEFT:
            self.keyboard['LEFT'] = 1
        elif key == arcade.key.RIGHT:
            self.keyboard['RIGHT'] = 1
        elif key == arcade.key.UP:
            self.keyboard['UP'] = 1
        elif key == arcade.key.DOWN:
            self.keyboard['DOWN'] = 1
        #TODO REMOVE FOR RELEASE
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        ''' called whenever the user releases a key'''
        if key == arcade.key.W:
            self.keyboard['W'] = 0
        elif key == arcade.key.S:
            self.keyboard['S'] = 0
        elif key == arcade.key.A:
            self.keyboard['A'] = 0
        elif key == arcade.key.D:
            self.keyboard['D'] = 0
        elif key == arcade.key.LEFT:
            self.keyboard['LEFT'] = 0
        elif key == arcade.key.RIGHT:
            self.keyboard['RIGHT'] = 0
        elif key == arcade.key.UP:
            self.keyboard['UP'] = 0
        elif key == arcade.key.DOWN:
            self.keyboard['DOWN'] = 0
        # Set the initial view
        self.show_view(self.game_view)
