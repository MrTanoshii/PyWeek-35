from typing import Optional
import arcade
from constants import CONSTANTS as C

class Player(arcade.Sprite):

    def __init__(self, keyboard: dict, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: arcade.Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)
        self.keyboard = keyboard
        self.facing_left = True
        self.last_facing = True
        self.textures = []
        texture = arcade.load_texture(filename, flipped_horizontally=True)
        self.textures.append(texture)
        texture = arcade.load_texture(filename)
        self.textures.append(texture)

    def update(self):   
        move_x = ((self.keyboard['D'] | self.keyboard['RIGHT'] * C.MOVEMENT_SPEED) - (self.keyboard['A'] | self.keyboard['LEFT'] * C.MOVEMENT_SPEED))
        move_y = ((self.keyboard['W'] | self.keyboard['UP'] * C.MOVEMENT_SPEED) - (self.keyboard['S'] | self.keyboard['DOWN'] * C.MOVEMENT_SPEED))
        penalty = 0.70710678118 if move_x and move_y else 1
        self.center_x += move_x * penalty
        self.center_y += move_y * penalty

        if move_x < 0:
            self.facing_left = True
        elif move_x > 0:
            self.facing_left = False
        
        if self.last_facing == self.facing_left:
            pass
        else:
            self.texture = self.textures[self.facing_left]
            self.last_facing = self.facing_left


        if self.left < 0:
            self.left = 0
        elif self.right > C.SCREEN_WIDTH -1:
            self.right = C.SCREEN_WIDTH -1
        if self.bottom < 0: 
            self.bottom = 0
        elif self.top > C.SCREEN_HEIGHT - 1:
            self.top = C.SCREEN_HEIGHT - 1
