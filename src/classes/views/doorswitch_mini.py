import arcade

from src.constants import CONSTANTS as C

class DoorSwitchMini(arcade.View):
    """Light Switch Mini Game"""
    def __init__(self):
        super().__init__()
        # self.window.show_view(self)
    
    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_text(
            "door switch",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass
