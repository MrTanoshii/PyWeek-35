from arcade import load_texture

from classes.interactables.interactable import Interactable


class Safe(Interactable):
    """Base class for safe interactables."""

    index_count = 1
    safe_list = []

    def __init__(self, name: str = "", description: str = "", *args, **kwargs):
        """
        Constructor.

        Keyword Arguments:
            name (str): Name of the safe. (default "")
            description (str): Description of the safe. (default "")
        """

        if not name:
            name = f"{type(self).__name__} #{Safe.index_count}"
            Safe.index_count += 1

        self.texture = load_texture("./src/assets/art/safe/usb.png")

        super().__init__(name, description, self, *args, **kwargs)

    def setup(self):
        """Setup."""

        Safe.safe_list.append(self)

        super().setup()

    def remove(self):
        """Delete the object."""

        super().remove()

        Safe.safe_list.remove(self)

    def interact(self):
        """
        Interact with the light switch.
        Overrides the parent class method.
        """

        pass
