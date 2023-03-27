from arcade import SpriteList


class InteractablesManager(object):
    """
    Base class for interactables manager.
    Singleton.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(InteractablesManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Constructor."""

        self.interactable_list = []
        self.interactable_spritelist = SpriteList()
