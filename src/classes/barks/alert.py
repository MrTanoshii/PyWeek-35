from arcade import load_texture

from src.classes.barks.bark import Bark


class Alert(Bark):
    def __init__(self, center_x: float, center_y: float, despawn_timer: float = 1.0):
        """Constructor."""

        # Inherit parent class
        super().__init__(center_x, center_y, despawn_timer=despawn_timer)
        self.texture=load_texture("src/assets/vfx/alert.png")
        self.scale=1.5
