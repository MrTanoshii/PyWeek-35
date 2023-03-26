import arcade

from constants import CONSTANTS as C
from classes.interactables.light_switch import LightSwitch


class GameView(arcade.View):
    """Base class for the 'game' view."""

    def __init__(self):
        super().__init__()

        self.setup()

    def setup(self):
        """Set up the view."""

        self.light_switch = LightSwitch()
        self.light_switch.center_x = C.SCREEN_WIDTH / 2
        self.light_switch.center_y = C.SCREEN_HEIGHT / 2
        self.light_switch.scale = 0.05

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the view."""
        self.clear()

        arcade.draw_text(
            "Files retrieved: 0/0",
            10,
            C.SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="left",
            anchor_y="center",
        )

        self.light_switch.draw()

    def update(self, delta_time: float):
        self.light_switch.update()

        return super().update(delta_time)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass
