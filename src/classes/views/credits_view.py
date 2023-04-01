import arcade

import arcade.gui as GUI

from src.constants import CONSTANTS as C


class CreditsView(arcade.View):
    """Base class for the 'credits' view."""

    def __init__(self, ingamemenu_view):
        super().__init__()

        # Measurement variables
        text_height = 300
        text_width = 700
        button_width = 300
        button_bottom = 20

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = GUI.UIManager()
        self.manager.enable()

        # Create veritcal BoxGroup to align buttons
        self.v_box = GUI.UIBoxLayout()

        # Create UI elements
        credits_text = """
        This game was created by:

        - BJ
        - DL200032
        - DivineShadow777
        - EveryoneHATEme
        - Jeb
        - Krzysztof
        - M1ku
        - mihett05
        - MrTanoshii

        GitHub Repository: https://github.com/MrTanoshii/PyWeek-35/
        PyWeek Team:       https://pyweek.org/e/herewegoagain/
        """

        credits_text = GUI.UITextArea(
            text=credits_text,
            width=text_width,
            height=text_height,
        )
        back_button = GUI.UIFlatButton(text="Back", width=button_width)

        self.v_box.add(credits_text.with_space_around(bottom=button_bottom))
        self.v_box.add(back_button.with_space_around(bottom=button_bottom))

        # User decorators to handle on_click events

        # Exit the game
        @back_button.event("on_click")
        def on_click_back(event):
            self.window.show_view(ingamemenu_view)

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
