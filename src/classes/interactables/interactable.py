from arcade import Sprite
from classes.managers.game_manager import GameManager


class Interactable(Sprite):
    interactable_list = []

    def __init__(self, name: str, description: str, interactable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.interactable = interactable

    def __enter__(self):
        """Context manager entry."""
        Interactable.interactable_list.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit."""
        Interactable.interactable_list.remove(self)

    def on_update(self, delta_time: float):
        print("do something")

    def interact(self, key: str):
        """Must be overriden by child class."""
        player = GameManager.instance.player

        # The Entity is gonna be self
