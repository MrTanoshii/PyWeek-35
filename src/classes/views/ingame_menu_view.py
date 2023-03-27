import arcade
import arcade.gui as GUI

from constants import CONSTANTS as C


class IngameMenuView(arcade.View):
    """Base class for the 'ingame menu' view."""

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        button_width = 300
        button_bottom = 20

        self.clear()

        self.manager = GUI.UIManager()
        self.manager.enable()

        self.v_box = GUI.UIBoxLayout()

        resume_button = GUI.UIFlatButton(text="Resume", width=button_width)
        self.v_box.add(resume_button.with_space_around(bottom=button_bottom))

        options_button = GUI.UIFlatButton(text="Options", width=button_width)
        self.v_box.add(options_button.with_space_around(bottom=button_bottom))

        credits_button = GUI.UIFlatButton(text="Credits", width=button_width)
        self.v_box.add(credits_button.with_space_around(bottom=button_bottom))

        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.manager.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass
