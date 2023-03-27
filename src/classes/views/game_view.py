import arcade
from pytiled_parser.tiled_object import Rectangle
from typing import List

from constants import CONSTANTS as C
from classes.managers.light_manager import LightManager
from classes.wall import Wall
from classes.world import World
from classes.guard import Guard


class GameView(arcade.View):
    """Base class for the 'game' view."""

    def __init__(self):
        super().__init__()
        self.scene = None
        self.world = World.load("example.tilemap.json")
        self.guard = None
        self.light = LightManager()
        self.walls = arcade.SpriteList()
        self.physics_engine = None
        self.setup()
        self.last_pos = (0, 0)

    def setup(self):
        """Set up the view."""
        self.scene = arcade.Scene.from_tilemap(self.world.map)
        for wall in [
            Wall(
                wall.coordinates.x - wall.size.width / 2,
                self.window.height - wall.coordinates.y - wall.size.height / 2,
                wall.size.width, wall.size.height
            )
            for wall in self.world.walls
        ]:  # TODO: fix it
            self.walls.append(wall)

        self.guard = Guard()

        self.physics_engine = arcade.PhysicsEngineSimple(self.guard, self.walls)

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.ARMY_GREEN)

    def on_draw(self):
        """Draw the view."""
        # Primary camera stuff here:

        self.light.on_draw_shadows()
        # Draw fragments which shouldn't pass the light:
        self.walls.draw()

        self.light.on_draw()
        # Draw fragments which can be in the shadow:
        self.scene.draw()

        arcade.get_window().use()
        self.clear()
        self.light.on_draw_shader(self.last_pos[0], self.last_pos[1])

        self.guard.draw()

        self.walls.draw()

        arcade.draw_text(
            "Files retrieved: 0/0",
            10,
            C.SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            font_size=30,
            font_name="Minecraft",
            anchor_x="left",
            anchor_y="center",
        )

    def on_update(self, delta_time: float):
        """Update the view."""
        self.physics_engine.update()
        self.scene.update()
        self.guard.update(delta_time)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        self.guard.on_key_press(key, modifiers)

    def on_resize(self, width: int, height: int):
        self.light.on_resize(width, height)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.last_pos = (x, y)
