from arcade import load_texture
from .interactable import Interactable


class LightSwitch(Interactable):
    """Base class for light switch interactables."""

    light_switch_list = []

    def __init__(self, name: str = "", description: str = "", *args, **kwargs):
        """_summary_

        Args:
            name (str): Name of the light switch.
            description (str): Optional description of the light switch.
        """
        if not name:
            name = f"Light Switch #{len(LightSwitch.light_switch_list)}"
        super().__init__(name, description, self, *args, **kwargs)

        self.texture_on = load_texture(
            "./src/assets/art/light_switch/light_switch_on.png"
        )
        self.texture_off = load_texture(
            "./src/assets/art/light_switch/light_switch_off.png"
        )

        self.is_on = False
        LightSwitch.light_switch_list.append(self)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit."""
        LightSwitch.light_switch_list.remove(self)

    def update(self):
        super().update()

        # Update sprite based on light switch state
        self.texture = self.texture_on if self.is_on else self.texture_off
        # print(f"The texture is {self.texture}.")

    def interact(self):
        """Interact with the light switch.
        Overrides the parent class method."""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        """Turn on the light switch."""
        self.is_on = True
        print(f"Light switch ({self.name}) turned on.")

    def turn_off(self):
        """Turn off the light switch."""
        self.is_on = False
        print(f"Light switch ({self.name}) turned off.")
