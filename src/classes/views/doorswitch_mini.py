import arcade

from src.constants import CONSTANTS as C


class DoorSwitchMini(arcade.View):
    """Light Switch Mini Game"""

    def __init__(self):
        super().__init__()
        # self.window.show_view(self)
        self.blue_wire = arcade.Sprite(
            "./src/assets/art/door_switch/doorswitch_mini_blue.png"
        )
        self.orange_wire = arcade.Sprite(
            "./src/assets/art/door_switch/doorswitch_mini_orange.png"
        )
        self.green_wire = arcade.Sprite(
            "./src/assets/art/door_switch/doorswitch_mini_green.png"
        )
        for sprite in [self.blue_wire, self.orange_wire, self.green_wire]:
            sprite.center_x = C.SCREEN_WIDTH / 2
            sprite.center_y = C.SCREEN_HEIGHT / 2

        self.next_wire_timer = 0

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

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

        if self.next_wire_timer <= 0:
            # Change to next texture and wire
            pass
        else:
            self.next_wire_timer -= delta_time
