import math
from random import randint

import arcade

import os.path

from src.classes.managers.game_manager import GameManager
from src.constants import CONSTANTS as C


def calculate_angle(x1, y1, x2, y2):
    """Calculate the angle between two points"""
    return math.atan2(y2 - y1, x2 - x1)


def get_distance_between_coords(x1, y1, x2, y2):
    """Get the distance between two coordinates"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_direction_from_angle(angle):
    if abs(math.cos(angle)) > abs(math.sin(angle)):
        if math.cos(angle) > 0:
            direction = "right"
        elif math.cos(angle) < 0:
            direction = "left"
    else:
        if math.sin(angle) > 0:
            direction = "up"
        elif math.sin(angle) < 0:
            direction = "down"

    return direction


class Guard(arcade.Sprite):
    def __init__(self):
        # Inherit parent class
        super().__init__()

        self.name = ""

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
        self.is_colliding = False

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

        self.view_distance = None

        self.game_manager = GameManager()

        # Setup
        self.setup()

    def setup(self):
        # Configure Sprite
        self.center_x = 100
        self.center_y = 100
        self.scale = 0.2 * C.WORLD_SCALE

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
            "left": self.texture_list[24:48],
            "up": self.texture_list[72:96],
            "down": self.texture_list[0:24],
            "right": self.texture_list[48:64],
        }

        self.collision_list = self.game_manager.walls

        # Configure Movement
        self.speed = 3

        # Configure AI
        self.is_patrolling = True
        self.view_distance = 300

        self.game_manager.guards.append(self)

        self.name = f"guard_{len(self.game_manager.get_guards())}"

    def on_update(self, dt):
        if not self.patrol_points:
            self.get_patrolling_points()

        """Animation"""
        self.animation_counter += self.animation_speed
        if self.animation_counter > 1:
            self.update_animation()
            self.animation_counter = 0

        self.is_colliding = arcade.check_for_collision_with_list(self, self.collision_list)

        # calculate the angle between the guard and the player
        angle = calculate_angle(
            self.center_x,
            self.center_y,
            self.game_manager.player.center_x,
            self.game_manager.player.center_y,
        )

        # calculate the distance between the guard and the player
        distance = get_distance_between_coords(
            self.center_x,
            self.center_y,
            self.game_manager.player.center_x,
            self.game_manager.player.center_y,
        )

        # if the guard is close enough to the player
        if distance < self.view_distance and self.direction == get_direction_from_angle(angle) or distance < 150:

            if distance < 100:
                print("Game Over")

            # if the guard is not colliding with a wall
            if not self.is_colliding:

                # set the guard to chase the player
                self.is_chasing = True
                self.is_patrolling = False
                self.chase_target = self.game_manager.player
                self.chase_target_last_pos = (self.chase_target.center_x, self.chase_target.center_y)

            # if the guard is colliding with a wall
            else:

                # set the guard to patrol
                self.is_chasing = False
                self.is_patrolling = True
                self.chase_target = None
                self.chase_target_last_pos = None

        else:
            self.is_chasing = False
            self.is_patrolling = True
            self.chase_target = None
            self.chase_target_last_pos = None

        # If the guard is patrolling
        if self.is_patrolling:
            self.patrol()

        # move the guard towards the player
        elif self.is_chasing:
            self.chase()

    def update_animation(self):
        """Update the animated texture"""
        self.texture = self.next_item(self.animation_map[self.direction], self.current_texture_index)

    def next_item(self, lst: list[arcade.Texture], idx: int):
        """Get the next item in a looping list"""
        self.current_texture_index = (idx + 1) % len(lst)
        return lst[self.current_texture_index]

    def patrol(self):
        """Patrol between the patrol points"""

        # Calculate angle to patrol point
        angle = calculate_angle(
            self.center_x,
            self.center_y,
            self.patrol_points[self.patrol_index][0],
            self.patrol_points[self.patrol_index][1],
        )

        if not self.is_colliding:
            # Move towards patrol point
            self.center_x += math.cos(angle) * self.speed
            self.center_y += math.sin(angle) * self.speed

        self.direction = get_direction_from_angle(angle)

        # If the guard is close enough to the patrol point

        if (
            get_distance_between_coords(
                self.center_x,
                self.center_y,
                self.patrol_points[self.patrol_index][0],
                self.patrol_points[self.patrol_index][1],
            )
            < 5
        ):
            # Change patrol point
            self.patrol_index = self.get_next_patrol_point()

    def chase(self):
        """Chase the target"""

        # Calculate angle to target
        angle = calculate_angle(
            self.center_x,
            self.center_y,
            self.chase_target.center_x,
            self.chase_target.center_y,
        )

        if not self.is_colliding:
            # Move towards target
            self.center_x += math.cos(angle) * self.speed * 3
            self.center_y += math.sin(angle) * self.speed * 3

        self.direction = get_direction_from_angle(angle)

        # If the guard is close enough to the target
        if (
            get_distance_between_coords(
                self.center_x,
                self.center_y,
                self.chase_target.center_x,
                self.chase_target.center_y,
            )
            < 5
        ):
            # Set the guard to patrol
            self.is_chasing = False
            self.is_patrolling = True
            self.chase_target = None
            self.chase_target_last_pos = None

    def get_patrolling_points(self):
        path = self.game_manager.world.guard_patrol_points
        for point in path:
            # Point(id=40, coordinates=OrderedPair(x=288, y=192), name='guard_1', properties={'path': 41})
            if point.name == self.name:
                _x = (point.coordinates.x + point.size.width / 2) * C.WORLD_SCALE
                _y = (
                    self.game_manager.world.height * self.game_manager.world.tile_size
                    - point.coordinates.y
                    - point.size.height / 2
                ) * C.WORLD_SCALE
                self.patrol_points.append((_x, _y))

    def get_next_patrol_point(self):
        """Get the next patrol point"""
        self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
        return self.patrol_index
