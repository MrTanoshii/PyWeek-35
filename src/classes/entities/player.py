import math
import os
from typing import Optional
import arcade
from src.constants import CONSTANTS as C


class Player(arcade.Sprite):
    def __init__(
        self,
        game_manager,
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
        # self.game_manager = GameManager() DOES NOT WORK SINGLETON IS FUCKED
        self.keyboard = keyboard
        self.facing_left = True
        self.last_facing = True
        self.game_manager = game_manager

        base_path = f"src/assets/animations/cat"

        self.texture_list_left = [
            arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm="Simple")
            for texture in os.listdir(base_path)
        ]

        self.texture_list_right = [
            arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm="Simple", flipped_horizontally=True)
            for texture in os.listdir(base_path)
        ]

        self.texture_list_up = [
            arcade.load_texture(f"{base_path}2/{texture}", hit_box_algorithm="Simple")
            for texture in os.listdir(base_path+"2")
        ]

        self.texture_list_down = [
            arcade.load_texture(f"{base_path}3/{texture}", hit_box_algorithm="Simple")
            for texture in os.listdir(base_path+"3")
        ]

        self.texture_options = [self.texture_list_left, self.texture_list_right, self.texture_list_up, self.texture_list_down]
        self.texture = self.texture_list_left[0]

        self.current_texture = self.texture_list_left
        self.animation_speed = 48 / 60
        self.animation_counter = 0
        self.current_texture_index = 0
        self.scale = 0.5 * C.WORLD_SCALE

    def on_update(self, delta_time):

        move_x = ((self.keyboard["D"] | self.keyboard["RIGHT"]) * C.MOVEMENT_SPEED) - (
            (self.keyboard["A"] | self.keyboard["LEFT"]) * C.MOVEMENT_SPEED
        )
        move_y = ((self.keyboard["W"] | self.keyboard["UP"]) * C.MOVEMENT_SPEED) - (
            (self.keyboard["S"] | self.keyboard["DOWN"]) * C.MOVEMENT_SPEED
        )
        # Pythagorean theorem
        penalty = C.ONE_DIVIDED_BY_ROOT_TWO if move_x and move_y else 1
        self.center_x += move_x * penalty
        self.center_y += move_y * penalty

        if move_x < 0:
            self.current_texture = self.texture_list_right
        elif move_x > 0:
            self.current_texture = self.texture_list_left
        elif move_y > 0:
            self.current_texture = self.texture_list_up
        elif move_y < 0:
            self.current_texture = self.texture_list_down

        if not move_y and not move_x:
            self.animation_speed = 0
        else:
            self.animation_speed = 40/60

        # This is to prevent the player from flipping back and forth
        if self.last_facing == self.facing_left:
            pass
        else:
            # This is to flip the player
            self.current_texture = self.texture_options[self.facing_left]
            self.last_facing = self.facing_left

        # collisions = arcade.check_for_collision_with_list(self, self.game_manager.walls)
        # for wall in collisions:
        # IDK which is more efficient or if there is a difference.
        for wall in self.game_manager.walls:
            if wall.collides_with_sprite(self):
                if self.right >= wall.left and self.right - wall.left < C.PLAYER_COLLISION_THRESHOLD:
                    self.right = wall.left
                elif self.left <= wall.right and wall.right - self.left < C.PLAYER_COLLISION_THRESHOLD:
                    self.left = wall.right
                if self.top >= wall.bottom and self.top - wall.bottom < C.PLAYER_COLLISION_THRESHOLD:
                    self.top = wall.bottom
                elif self.bottom <= wall.top and wall.top - self.bottom < C.PLAYER_COLLISION_THRESHOLD:
                    self.bottom = wall.top
        self.animation_counter += self.animation_speed
        if self.animation_counter > 1:
            self.update_animation()
            self.animation_counter = 0

        self.game_manager.player_in_light = self.check_if_player_in_light()

    def update_animation(self):
        """Update the animated texture"""
        self.texture = self.next_item(self.current_texture, self.current_texture_index)

    def next_item(self, lst, idx):
        """Get next item in texture list"""
        self.current_texture_index = (idx + 1) % len(lst)
        return lst[self.current_texture_index]

    def check_if_player_in_light(self):
        """Check if player is in light"""
        for light in self.game_manager.lights:
            # calculate if player is inside circle
            light_x = light.center_x
            light_y = light.center_y
            if light.light_radius > math.sqrt((self.center_x - light_x)**2 + (self.center_y - light_y)**2):
                return True
        return False

