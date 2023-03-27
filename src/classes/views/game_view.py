import arcade

from constants import CONSTANTS as C
from classes.interactables.interactable import Interactable
from classes.interactables.light_switch import LightSwitch
from classes.managers.game_manager import GameManager
from classes.managers.interactables_manager import InteractablesManager


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

        # TODO: Uncomment when player is implemented
        # GameManager.instance.player.draw()
        InteractablesManager.instance.interactable_spritelist.draw()

    def update(self, delta_time: float):
        return super().update(delta_time)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass

    # TODO: This should be in player, not here
    def on_key_release(self, key, modifiers):
        player = GameManager.instance.player

        # TODO: For testing only, remove this player initialisation
        if player is None:
            GameManager.instance.set_player(
                arcade.Sprite(
                    "./src/assets/art/light_switch/light_switch_off.png",
                    0.3,
                    center_x=600,
                    center_y=445,
                )
            )

        if key == arcade.key.E:
            player = GameManager.instance.player
            interactables = arcade.check_for_collision_with_list(
                player, InteractablesManager.instance.interactable_spritelist
            )

            for interactable in interactables:
                interactable.interact()
