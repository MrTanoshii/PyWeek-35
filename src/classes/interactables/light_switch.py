import arcade
from arcade import load_texture

from src.classes.interactables.interactable import Interactable
from src.classes.interactables.minigame import MiniGame
from src.classes.views.lightswitch_mini import LightSwitchMini
from src.classes.managers.game_manager import GameManager


class LightSwitch(Interactable):
    """Base class for light switch interactables."""

    index_count = 1
    light_switch_list = []

    def __init__(self, name: str = "", description: str = "", *args, **kwargs):
        """
        Constructor.

        Keyword Arguments:
            name (str): Name of the light switch. (default "")
            description (str): Description of the light switch. (default "")
        """

        if not name:
            name = f"{type(self).__name__} #{LightSwitch.index_count}"
            LightSwitch.index_count += 1

        self.texture_on = load_texture(
            "./src/assets/art/light_switch/light_switch_on.png"
        )
        self.texture_off = load_texture(
            "./src/assets/art/light_switch/light_switch_off.png"
        )
        self.is_on = False
        self.game_manager = GameManager.instance
        self.player_collides = False
        self.lights = []

        super().__init__(name, description, self, *args, **kwargs)

    def setup(self):
        """Setup."""

        self.update_texture()
        LightSwitch.light_switch_list.append(self)
        self.scale = 0.1
        super().setup()

    def remove(self):
        """Delete the object."""

        super().remove()

        LightSwitch.light_switch_list.remove(self)

    def check_lights(self):
        for light in self.lights:
            if light.enabled:
                return True
        return False

    def interact(self):
        """
        Interact with the light switch.
        Overrides the parent class method.
        """
        if self.check_lights():
            MiniGame(LightSwitchMini())
            self.turn_off()
        else:
            self.turn_on()

        self.update_texture()

    def update_texture(self):
        """Update the texture of the light switch."""

        self.texture = self.texture_on if self.is_on else self.texture_off

    def turn_on(self):
        """Turn on the light switch."""
        for light in self.lights:
            if not light.enabled:
                light.toggle()
                arcade.Sound("./src/assets/light_sfx/SwitchOn.ogg").play()
        # print(f"{self.name} turned on.")

    def turn_off(self):
        """Turn off the light switch."""
        for light in self.lights:
            # print(light, light.enabled)
            if light.enabled:
                # print("turning off")
                light.toggle()
                # print(light.enabled)
        # print(f"{self.name} turned off.")

    def on_update(self, delta_time: float = 1 / 60):
        """Update the light switch."""
        player = self.game_manager.player

        # Check collision
        if arcade.check_for_collision(self, player):
            self.player_collides = True
        else:
            self.player_collides = False

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key == arcade.key.E:
            if self.player_collides:
                self.interact()
