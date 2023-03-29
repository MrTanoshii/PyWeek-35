from random import randint

import arcade

import os.path

from src.classes.managers.game_manager import GameManager
from src.constants import CONSTANTS as C


class Guard(arcade.Sprite):
    def __init__(self):
        # Inherit parent class
        super().__init__()

        # Init Assets
        self.texture_list = []
        self.animation_path = f"src/assets/animations/guard/"

        # Init Animation
        self.current_texture: float = 0
        self.animation_speed: float = 0
        self.current_texture_index: int = 0
        self.animation_counter: int = 0
        self.texture = None
        self.animation_map = None
        self.direction = None

        # Init Physics
        self.collision_list = None

        # Init Movement
        self.target = None
        self.speed: float = 0
        self.max_speed: float = 0

        # Init AI
        self.is_alerted = False
        self.is_chasing = False
        self.is_patrolling = False
        self.assigned_light_switch = None

        self.patrol_points = []
        self.patrol_index = 0

        self.chase_target = None
        self.chase_target_last_pos = None

        self.game_manager = GameManager()

        # Setup
        self.setup()

    def setup(self):
        # Configure Sprite
        self.center_x = 100
        self.center_y = 100
        self.scale = 0.5 * C.WORLD_SCALE

        # Load animation textures
        self.texture_list = [
            arcade.load_texture(f"{self.animation_path}/{texture}", hit_box_algorithm="Simple")
            for texture in os.listdir(self.animation_path)
        ]

        # Set initial texture
        self.texture = self.texture_list[0]

        # Configure Animation
        self.animation_speed: float = 24 / 60
        self.direction = "idle"

        self.animation_map = {
            "idle": self.texture_list[12:13],
            "left": self.texture_list[0:24],
            "up": self.texture_list[0:24],
            "down": self.texture_list[0:24],
            "right": self.texture_list[24:48],
        }

        self.collision_list = self.game_manager.walls

        self.game_manager.guards.append(self)

    def on_update(self, dt):

        """Animation"""
        self.animation_counter += self.animation_speed
        if self.animation_counter > 1:
            self.update_animation()
            self.animation_counter = 0

        is_colliding = arcade.check_for_collision_with_list(self, self.collision_list)

    def update_animation(self):
        """Update the animated texture"""
        self.texture = self.next_item(self.animation_map[self.direction], self.current_texture_index)

    def next_item(self, lst: list[arcade.Texture], idx: int):
        """Get the next item in a looping list"""
        self.current_texture_index = (idx + 1) % len(lst)
        return lst[self.current_texture_index]
