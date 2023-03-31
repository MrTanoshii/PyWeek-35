import math
import arcade


class CONSTANTS:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    SCREEN_TITLE = "Shadow Heist v0.0.3 - PyWeek 35"
    BACKGROUND_COLOR = arcade.color.BLACK
    MOVEMENT_SPEED = 10
    WORLD_SCALE = 4.0
    DEFAULT_LIGHT_RADIUS = 300
    PLAYER_COLLISION_THRESHOLD = 25
    ONE_DIVIDED_BY_ROOT_TWO = 1 / math.sqrt(2)


arcade.load_font("src/assets/fonts/pixel.ttf")  # MODERN WARFARE
arcade.load_font("src/assets/fonts/font.ttf")  # Minecraft