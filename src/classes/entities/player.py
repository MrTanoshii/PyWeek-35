import math
import os
from typing import Optional
import arcade
from src.constants import CONSTANTS as C


class Player(arcade.Sprite):
    def __init__(
        self,
        keyboard: dict,
        filename: str = None,
        scale: float = 1,
        image_x: float = 0,
        image_y: float = 0,
        image_width: float = 0,
        image_height: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        repeat_count_x: int = 1,
        repeat_count_y: int = 1,
        flipped_horizontally: bool = False,
        flipped_vertically: bool = False,
        flipped_diagonally: bool = False,
        hit_box_algorithm: Optional[str] = "Simple",
        hit_box_detail: float = 4.5,
        texture: arcade.Texture = None,
        angle: float = 0,
    ):
        super().__init__(
            filename,
            scale,
            image_x,
            image_y,
            image_width,
            image_height,
            center_x,
            center_y,
            repeat_count_x,
            repeat_count_y,
            flipped_horizontally,
            flipped_vertically,
            flipped_diagonally,
            hit_box_algorithm,
            hit_box_detail,
            texture,
            angle,
        )
        self.keyboard = keyboard
        self.facing_left = True
        self.last_facing = True
        texture = arcade.load_texture(filename, flipped_horizontally=True)
      

        base_path = f"src/assets/animations/panda/"

        self.texture_list_left = [
            arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm="Simple")
            for texture in os.listdir(base_path)
        ]
        
        self.texture_list_right = [
            arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm="Simple", flipped_horizontally=True)
            for texture in os.listdir(base_path)
        ]
        self.texture_options = [self.texture_list_left, self.texture_list_right]

        self.current_texture = self.texture_list_left
        self.animation_speed = 48/60
        self.animation_counter = 0
        self.current_texture_index = 0
  
    def on_update(self, delta_time):
        move_x = ((self.keyboard["D"] | self.keyboard["RIGHT"]) * C.MOVEMENT_SPEED) - (
            (self.keyboard["A"] | self.keyboard["LEFT"]) * C.MOVEMENT_SPEED
        )
        move_y = ((self.keyboard["W"] | self.keyboard["UP"]) * C.MOVEMENT_SPEED) - (
            (self.keyboard["S"] | self.keyboard["DOWN"]) * C.MOVEMENT_SPEED
        )
        # Pythagorean theorem
        penalty = 1 / math.sqrt(2) if move_x and move_y else 1
        self.center_x += move_x * penalty
        self.center_y += move_y * penalty

        if move_x < 0:
            self.facing_left = True
            self.current_texture = self.texture_list_left
        elif move_x > 0:
            self.facing_left = False
            self.current_texture = self.texture_list_right

        # This is to prevent the player from flipping back and forth
        if self.last_facing == self.facing_left:
            pass
        else:
            # This is to flip the player
            # self.texture = self.textures[self.facing_left]
            self.current_texture = self.texture_options[self.facing_left]
            self.last_facing = self.facing_left


        self.animation_counter += self.animation_speed
        if self.animation_counter > 1:
            self.update_animation()
            self.animation_counter = 0
    
        ### This binds the player to the screen
        # if self.left < 0:
        #     self.left = 0
        # elif self.right > C.SCREEN_WIDTH - 1:
        #     self.right = C.SCREEN_WIDTH - 1
        # if self.bottom < 0:
        #     self.bottom = 0
        # elif self.top > C.SCREEN_HEIGHT - 1:
        #     self.top = C.SCREEN_HEIGHT - 1



    def update_animation(self):
        """Update the animated texture"""
        self.texture = self.next_item(self.current_texture, self.current_texture_index)
    def next_item(self, lst, idx):
        self.current_texture_index = (idx + 1) % len(lst)
        return lst[self.current_texture_index]
