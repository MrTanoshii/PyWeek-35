from arcade import load_texture
import arcade

from src.classes.interactables.interactable import Interactable
from src.classes.interactables.minigame import MiniGame
from src.classes.views.safe_mini import SafeMini
from src.classes.managers.game_manager import GameManager


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

        self.safe_texture = load_texture("./src/assets/art/safe/usb.png")
        self.is_completed = None
        self.game_manager = GameManager.instance
        self.player_collides = False
        self.interaction_time = None

        super().__init__(name, description, self, *args, **kwargs)

    def setup(self):
        """Setup."""

        self.set_texture()
        Safe.safe_list.append(self)

        super().setup()

    def remove(self):
        """Delete the object."""

        super().remove()

        Safe.safe_list.remove(self)

    # TODO: texture works like this for some reason
    def set_texture(self):
        self.texture = self.safe_texture

    def interact(self):
        """
        Interact with the light switch.
        Overrides the parent class method.
        """
        if self.is_completed == None:
            MiniGame(SafeMini(self))

        # Lose but can continue
        elif not self.is_completed and self.game_manager.time >= self.interaction_time:
            print("You lost, but can continue")
            MiniGame(SafeMini(self))
        
        elif self.is_completed:
            print("You already won")
            
        # Win
        # TODO: Remove the sprite and add to inventory list 
        else:
            print(self.game_manager.time, self.interaction_time)
            # print("WIN")
    
    def on_update(self, delta_time: float = 1/60):
        """Update the safe."""
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
                    # print("collided with safe!")
                    self.interact()
