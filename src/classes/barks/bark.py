from arcade import Sprite

from src.classes.managers.game_manager import GameManager


class Bark(Sprite):
    def __init__(self, center_x, center_y, despawn_timer: float):
        """Constructor."""

        print("This is BEING RUN")
        # Inherit parent class
        super().__init__()

        self.despawn_timer = despawn_timer
        self._hit_box_algorithm = None
        self.center_x = center_x
        self.center_y = center_y
        GameManager.instance.barks.append(self)

    def on_update(self, delta_time: float = 1 / 60):
        """Update the bark.

        Keyword arguments:
        delta_time -- The time since the last update (default 1/60)
        """

        self.despawn_timer -= delta_time
        if self.despawn_timer <= 0:
            GameManager.instance.barks.remove(self)
            self.kill()

        return super().on_update(delta_time)
