import arcade

import os.path

from classes.managers.game_manager import GameManager


class Guard(arcade.Sprite):

    # SpriteList class attribute
    enemy_list = arcade.SpriteList()

    def __init__(self):
        # Inherit parent class

        super().__init__()

        """ Load Assets """
        base_path = f"assets/animations/guard/"

        # Load texture
        self.texture_list = []

        # Load all textures in folder
        self.texture_list = [arcade.load_texture(f"{base_path}/{texture}", hit_box_algorithm="Simple") for texture in os.listdir(base_path)]

        self.current_texture: float = 0
        self.animation_speed: float = 24 / 60

        # Set the initial texture
        self.current_texture_index = 0
        self.texture = self.texture_list[self.current_texture_index]

        self.animation_list = {
            "idle": self.texture_list[12:13],
            "left": self.texture_list[0:24],
            "up": self.texture_list[0:24],
            "down": self.texture_list[0:24],
            "right": self.texture_list[24:48],
        }
        self.status = None

        self.setup()

    def setup(self):
        # Add to SpriteList
        self.enemy_list.append(self)
        self.center_x = 100
        self.center_y = 100
        self.status = "right"
        self.scale = 1.0
        self.animation_counter = 0
        self.animation_speed = 24 / 60

    @ classmethod
    def update(cls, dt: float):
        walls = GameManager.instance.collision
        # Cycle trough all enemies
        for enemy in cls.enemy_list:
            # Move all Enemies Forwards
            if enemy.status == "left":
                # Check collision with wall
                if enemy.center_x <= 100:
                    enemy.status = "right"
                enemy.center_x -= 60 * dt
            elif enemy.status == "right":
                # Check collision with wall
                if enemy.center_x >= 1000:
                    enemy.status = "left"
                enemy.center_x += 60 * dt
            elif enemy.status == "up":
                # Check collision with wall
                if enemy.center_y >= 700:
                    enemy.status = "down"
                enemy.center_y += 60 * dt
            elif enemy.status == "down":
                # Check collision with wall
                if enemy.center_y <= 100:
                    enemy.status = "up"
                enemy.center_y -= 60 * dt
            # Update animation every 2nd frame
            enemy.animation_counter += enemy.animation_speed
            if enemy.animation_counter > 1:
                enemy.update_animation()
                enemy.animation_counter = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.status = "left"
        elif key == arcade.key.RIGHT:
            self.status = "right"
        elif key == arcade.key.UP:
            self.status = "up"
        elif key == arcade.key.DOWN:
            self.status = "down"

    def update_animation(self):
        """ Update the animated texture """
        self.texture = self.next_item(self.animation_list[self.status], self.current_texture_index)

    def next_item(self, lst: list[arcade.Texture], idx: int):
        """ Get the next item in a looping list"""
        self.current_texture_index = (idx + 1) % len(lst)
        return lst[self.current_texture_index]

