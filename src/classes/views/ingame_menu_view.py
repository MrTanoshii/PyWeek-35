import arcade
import arcade.gui as GUI

from src.constants import CONSTANTS as C


class IngameMenuView(arcade.View):
    """Base class for the 'ingame menu' view."""

    def __init__(self):
        super().__init__()

        # Measurement variables
        button_width = 300
        button_bottom = 20

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = GUI.UIManager()
        self.manager.enable()

        # Create veritcal BoxGroup to align buttons
        self.v_box = GUI.UIBoxLayout()

        # Create buttons
        resume_button = GUI.UIFlatButton(text="Resume", width=button_width)
        options_button = GUI.UIFlatButton(text="Options", width=button_width)
        credits_button = GUI.UIFlatButton(text="Credits", width=button_width)
        quit_button = GUI.UIFlatButton(text="Quit", width=button_width)

        button_lst = [resume_button, options_button, credits_button, quit_button]
        for button in button_lst:
            self.v_box.add(button.with_space_around(bottom=button_bottom))

        # User decorators to handle on_click events
        @resume_button.event("on_click")
        def on_click_resume(event):
            print("Resume button clicked: ", event)

        @options_button.event("on_click")
        def on_click_options(event):
            print("Options button clicked: ", event)

        @credits_button.event("on_click")
        def on_click_credits(event):
            print("Credits button clicked: ", event)

        @quit_button.event("on_click")
        def on_click_quit(event):
            print("Quit button clicked: ", event)
            arcade.exit()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass
