import os
import arcade
from random import randint
from src.constants import CONSTANTS as C

class ServerLight(arcade.Sprite):

    servers = arcade.SpriteList()

    """server light"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_path = "src/assets/server_lights"
        self.texture_list = [arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm=None) for texture in os.listdir(base_path)]
        self.change_texture()
        self.servers.append(self)
        self.center_x = 0
        self.center_y = 0
        self.scale = C.WORLD_SCALE


    def change_texture(self):
        self.texture = self.texture_list[randint(0, len(self.texture_list) - 1)]
        self.color = (randint(128,255), 0, 0) if randint(0, 1) else (0, randint(128,255), 0)

    def on_update(self, delta_time: float = 1 / 60):
        if randint(0, 20) < 1:
            self.change_texture()
        return super().on_update(delta_time)
    

    def draw(self):
        super().draw()