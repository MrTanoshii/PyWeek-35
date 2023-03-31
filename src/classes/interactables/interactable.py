from arcade import Sprite

from src.classes.managers.interactables_manager import InteractablesManager


class Interactable(Sprite):
    """Base class for interactables."""

    def __init__(self, name: str, description: str, interactable, *args, **kwargs):
        """
        Constructor.

        Keyword Arguments:
            name (str): Name of the interactable.
            description (str): Description of the interactable.
            interactable (Interactable): The interactable object.
        """

        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.interactable = interactable

        self.setup()

    def setup(self):
        """Setup."""

        InteractablesManager.instance.interactable_list.append(self)
        InteractablesManager.instance.interactable_spritelist.append(self)

    def remove(self):
        """Delete the object."""

        InteractablesManager.instance.interactable_list.remove(self)
        InteractablesManager.instance.interactable_spritelist.remove(self)

    def interact(self):
        """Must be overriden by child class."""

        pass
