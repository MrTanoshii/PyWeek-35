from arcade import load_texture

from classes.interactables.interactable import Interactable


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

        super().__init__(name, description, self, *args, **kwargs)

    def setup(self):
        """Setup."""

        self.update_texture()
        LightSwitch.light_switch_list.append(self)

        super().setup()

    def remove(self):
        """Delete the object."""

        super().remove()

        LightSwitch.light_switch_list.remove(self)

    def interact(self):
        """
        Interact with the light switch.
        Overrides the parent class method.
        """

        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

        self.update_texture()

    def update_texture(self):
        """Update the texture of the light switch."""

        self.texture = self.texture_on if self.is_on else self.texture_off

    def turn_on(self):
        """Turn on the light switch."""
        self.is_on = True
        print(f"{self.name} turned on.")

    def turn_off(self):
        """Turn off the light switch."""
        self.is_on = False
        print(f"{self.name} turned off.")
