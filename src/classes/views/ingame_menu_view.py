import arcade

from constants import CONSTANTS as C


class IngameMenuView(arcade.View):
    """Base class for the 'ingame menu' view."""

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_text(
            "Menu Screen - click to advance",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        pass
