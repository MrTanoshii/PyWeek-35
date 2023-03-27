import arcade

from constants import CONSTANTS as C
from classes.guard import Guard
from classes.managers.game_manager import GameManager


class GameView(arcade.View):
    """Base class for the 'game' view."""

    def __init__(self):
        super().__init__()
        self.scene = None
        self.tilemap = None
        self.guard = None
        self.setup()

    def setup(self):
        """Set up the view."""
        self.tilemap = arcade.load_tilemap("assets/tilemaps/example.tilemap.json", scaling=1.25)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)
        self.collision = self.tilemap.get_tilemap_layer("paths")
        GameManager.instance.collision = self.collision


        self.guard = Guard()

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    @property
    def objects(self):
        return self.collision.tiled_objects

    def on_draw(self):
        """Draw the view."""
        self.clear()

        self.scene.draw()

        self.guard.draw()

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
        self.scene.update()
        self.guard.update(delta_time)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        self.guard.on_key_press(key, modifiers)
