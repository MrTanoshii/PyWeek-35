import arcade
from arcade import load_texture

from classes.interactables.interactable import Interactable
from src.classes.views.doorswitch_mini import DoorSwitchMini
from src.classes.interactables.minigame import MiniGame


class DoorSwitch(Interactable):
    """Base class for Door switch interactables."""

    index_count = 1
    door_switch_list = []

    def __init__(self, name: str = "", description: str = "", *args, **kwargs):
        """
        Constructor.

        Keyword Arguments:
            name (str): Name of the door switch. (default "")
            description (str): Description of the door switch. (default "")
        """

        if not name:
            name = fname = f"{type(self).__name__} #{DoorSwitch.index_count}"
            DoorSwitch.index_count += 1

        # TODO: change to door_switch_open.png/door_switch_close when asset available
        self.texture_on = load_texture(
            "./src/assets/art/light_switch/light_switch_on.png"
        )
        self.texture_off = load_texture(
            "./src/assets/art/light_switch/light_switch_off.png"
        )
        self.is_open = False

        super().__init__(name, description, self, *args, **kwargs)

    def setup(self):
        """Setup."""

        self.update_texture()
        DoorSwitch.door_switch_list.append(self)

        super().setup()

    def remove(self):
        """Delete the object."""

        self.update_texture()
        super().remove()

        DoorSwitch.door_switch_list.remove(self)
    
    def interact(self):
        """
        Interact with the door switch.
        Overrides the parent class method.
        """

        if self.is_open:
            self.close_door()
        else:
            MiniGame(DoorSwitchMini())
            self.open_door()

        self.update_texture()
    
    def update_texture(self):
        """Update the texture of the door switch."""
        self.texture = self.texture_on if self.is_open else self.texture_off

    def open_door(self):
        """Open the door."""
        self.is_open = True
        print(f"{self.name} is open.")

    def close_door(self):
        """Close the door."""
        self.is_open = False
        print(f"{self.name} is closed.")

        
    
