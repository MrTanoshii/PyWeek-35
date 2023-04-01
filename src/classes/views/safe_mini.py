import arcade
import arcade.gui as GUI
from src.classes.managers.game_manager import GameManager
from src.classes.managers.interactables_manager import InteractablesManager
import random

from src.constants import CONSTANTS as C


class SafeMini(arcade.View):
    """Safe Mini Game"""

    def __init__(self, parent):
        button_width = 90
        button_height = 60
        button_bottom = 25

        super().__init__()
        arcade.set_background_color(C.BACKGROUND_COLOR)
        # Assigning variables
        self.input = ""
        self.value1 = random.randint(0, 100)
        self.value2 = random.randint(0, 100)
        self.tries = 0
        self.is_not_full = True
        self.is_ended = False
        self.game_outcome = None
        self.parent = parent

        self.manager = GUI.UIManager()
        self.manager.enable()

        self.v_boxes = [GUI.UIBoxLayout(), GUI.UIBoxLayout(), GUI.UIBoxLayout()]

        # Create Buttons
        buttons = []
        for i in range(10):
            buttons.append(GUI.UIFlatButton(text=str(i), width=button_width, height=button_height))

        # Add buttons to the boxes
        for i, button in enumerate(buttons[1:]):
            self.v_boxes[i % 3].add(button.with_space_around(bottom=button_bottom))
        self.v_boxes[-2].add(buttons[0].with_space_around(bottom=button_bottom)) # Add the zero button

        # Add functions to buttons when pressed
        def make_func(index):
            def _function(event):
                if self.is_not_full:
                    self.input += str(index)
                    self.is_not_full = not len(self.input) == 5
            return _function
        for i, button in enumerate(buttons):
            button.on_click = make_func(i)

        # Creating buttons
        for i in range(len(self.v_boxes)):
            self.manager.add(
                GUI.UIAnchorWidget(
                    anchor_x="center",
                    align_x=-100 + (i * 100),
                    anchor_y="center",
                    align_y=-27 if i % 2 == 0 else -70,
                    child=self.v_boxes[i],
                )
            )

    # If user presses enter, check if the answer is correct
    # If correct, go back to game view
    # TODO: Add a way when won, player cant play minigame again
    def on_key_release(self, _symbol: int, _modifiers: int):
        if self.is_not_full and chr(self.key).isnumeric():
            self.input += chr(self.key)
            self.is_not_full = not len(self.input) == 5

        elif self.key == arcade.key.ENTER:
            if not self.is_ended:
                if self.tries >= 4:  # when no attempt left
                    self.game_outcome = "YOU LOSE!"
                    self.is_ended = True
                    self.parent.is_completed = False
                    self.parent.interaction_time = 5 + GameManager.instance.time
                else:
                    try: # Winning
                        if int(self.input) == self.value1 + self.value2:
                            self.game_outcome = "YOU WIN!"
                            GameManager.instance.score += 1
                            self.is_ended = True
                            self.parent.is_completed = True
                    except ValueError:
                        pass

                self.input = ""
                self.is_not_full = True
                self.tries += 1
            else:
                self.window.show_view(GameManager.instance.get_game_view())

    def on_draw(self):
        self.clear()
        if not self.is_ended:
            arcade.draw_rectangle_filled(
                C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2, 300, 450, arcade.color.WHITE
            )
            self.draw_text(f"{self.input}", (-130, 140), arcade.color.BLUE, 30, ("left","center"))
            self.draw_text(f"{self.value1} + {self.value2} =", (-130, 200), arcade.color.BLACK, 15, ("left","center"))
            self.draw_text("Press Enter to validate answer", (0, -350), arcade.color.WHITE, 30, ("center","baseline"))
            self.manager.draw() # Draw buttons
        else:
            self.draw_text(f"MINIGAME COMPLETED", (0, 0), arcade.color.WHITE, 30, ("center","baseline"))
            self.draw_text(f"{self.game_outcome}", (0, -50), arcade.color.WHITE, 30, ("center","baseline"))
            self.draw_text("Press Enter to exit", (0, -300), arcade.color.WHITE, 20, ("center","baseline"))

    def draw_text(self, text, offset = (0, 0), color = arcade.color.WHITE, font_size = 30, anchor = ("left", "baseline")):
        return arcade.draw_text(
            f"{text}",
            C.SCREEN_WIDTH / 2 + offset[0],
            C.SCREEN_HEIGHT / 2 + offset[1],
            color,
            font_size=font_size,
            anchor_x=anchor[0],
            anchor_y=anchor[1],
        )