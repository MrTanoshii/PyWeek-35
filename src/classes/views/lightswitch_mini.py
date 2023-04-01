import arcade

from src.constants import CONSTANTS as C
from src.classes.managers.game_manager import GameManager


class LightSwitchMini(arcade.View):
    """Light Switch Mini Game"""

    SWITCH_SIZE = 0.5

    def __init__(self):
        super().__init__()

        self.switch_on = arcade.Sprite(
            "./src/assets/art/light_switch/light_switch_on.png",
            LightSwitchMini.SWITCH_SIZE,
        )
        self.switch_off = arcade.Sprite(
            "./src/assets/art/light_switch/light_switch_off.png",
            LightSwitchMini.SWITCH_SIZE,
        )

        self.off_sound = arcade.Sound("./src/assets/light_sfx/SwitchOff.ogg")

        for sprite in [self.switch_on, self.switch_off]:
            sprite.center_x = C.SCREEN_WIDTH / 2
            sprite.center_y = C.SCREEN_HEIGHT / 2

        self.is_pressed = None

        self.camera = arcade.Camera(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(C.BACKGROUND_COLOR)

    def on_draw(self):
        self.camera.use()
        self.clear()

        # Draw status of light
        light_status = "ON"
        if self.is_pressed:
            light_status = "OFF"
        arcade.draw_text(
            f"Lights are {light_status}",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2 + 200,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

        # Draw instructions
        if not self.is_pressed:
            arcade.draw_text(
                "Press 'Space' to turn off the lights",
                C.SCREEN_WIDTH / 2,
                C.SCREEN_HEIGHT / 2 - 200,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )

        # Draw exit instructions
        arcade.draw_text(
            "Press 'q' to exit",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2 - 250,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

        # Draw switch
        if self.is_pressed:
            self.switch_off.draw()
        else:
            self.switch_on.draw()

    def on_key_press(self, key, modifiers):
        """Handle key release events."""

        if key == arcade.key.SPACE and not self.is_pressed:
            self.off_sound.play()
            self.is_pressed = True

        if key == arcade.key.Q:
            resume_game = GameManager.instance.get_game_view()
            self.window.show_view(resume_game)
