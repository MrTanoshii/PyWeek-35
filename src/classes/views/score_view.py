import arcade

from src.classes.managers.game_manager import GameManager
from src.constants import CONSTANTS as C

class ScoreView(arcade.View):
    def __init__(self, game_view):
        """Base class for the 'score' view."""
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    # TODO: add a rating and a completion time
    def on_draw(self):
        """Draw the game over screen"""
        self.clear()
        self._draw_centered_text("Game Over", 54, 200)
        self._draw_centered_text(f"Score: {GameManager.instance.score}", 24, 75)
        self._draw_centered_text(f"Completion time:", 24, 0)
        self._draw_centered_text(f"Rating:", 24, -75)
        self._draw_centered_text("Press any key to restart", 12, -250)
        self._draw_centered_text("Press ESC to exit", 12, -300)

    def _draw_centered_text(self, text: str, font_size: int, y_offset: int):
        """Helper function to draw text centered on the screen"""
        x = C.SCREEN_WIDTH / 2
        y = C.SCREEN_HEIGHT / 2 + y_offset
        arcade.draw_text(text, x, y, arcade.color.WHITE, font_size, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        else:
            self.game_view.setup()
            self.window.show_view(self.game_view)
