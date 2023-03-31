import arcade
import arcade.gui as GUI
from classes.managers.game_manager import GameManager
import random

from constants import CONSTANTS as C


class SafeMini(arcade.View):
    """Safe Mini Game"""

    def __init__(self):
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
        self.num_flag = True

        self.manager = GUI.UIManager()
        self.manager.enable()

        self.v_box = GUI.UIBoxLayout()
        self.v_box2 = GUI.UIBoxLayout()
        self.v_box3 = GUI.UIBoxLayout()

        # Create Buttons
        butt1 = GUI.UIFlatButton(text="1", width=button_width, height=button_height)
        butt2 = GUI.UIFlatButton(text="2", width=button_width, height=button_height)
        butt3 = GUI.UIFlatButton(text="3", width=button_width, height=button_height)
        butt4 = GUI.UIFlatButton(text="4", width=button_width, height=button_height)
        butt5 = GUI.UIFlatButton(text="5", width=button_width, height=button_height)
        butt6 = GUI.UIFlatButton(text="6", width=button_width, height=button_height)
        butt7 = GUI.UIFlatButton(text="7", width=button_width, height=button_height)
        butt8 = GUI.UIFlatButton(text="8", width=button_width, height=button_height)
        butt9 = GUI.UIFlatButton(text="9", width=button_width, height=button_height)
        butt0 = GUI.UIFlatButton(text="0", width=button_width, height=button_height)

        # Add buttons to the boxes
        for button1, button2, button3 in zip(
            [butt1, butt4, butt7], [butt2, butt5, butt8, butt0], [butt3, butt6, butt9]
        ):
            self.v_box.add(button1.with_space_around(bottom=button_bottom))
            self.v_box2.add(button2.with_space_around(bottom=button_bottom))
            self.v_box3.add(button3.with_space_around(bottom=button_bottom))

        self.v_box2.add(butt0.with_space_around(bottom=button_bottom))

        # Add functions to buttons when pressed
        @butt1.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "1"

        @butt2.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "2"

        @butt3.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "3"

        @butt4.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "4"

        @butt5.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "5"

        @butt6.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "6"

        @butt7.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "7"

        @butt8.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "8"

        @butt9.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "9"

        @butt0.event("on_click")
        def on_click(event):
            if self.num_flag:
                self.input += "0"

        # TODO: Issue here with anchor_x and anchor_y
        # Creating buttons
        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center",
                align_x=-100,
                anchor_y="center",
                align_y=-27,
                child=self.v_box,
            )
        )
        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center",
                align_x=0,
                anchor_y="center",
                align_y=-70,
                child=self.v_box2,
            )
        )
        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center",
                align_x=100,
                anchor_y="center",
                align_y=-27,
                child=self.v_box3,
            )
        )

    # If user presses enter, check if the answer is correct
    # If correct, go back to game view
    # TODO: Add a way when won, player cant play minigame again
    def on_key_release(self, _symbol: int, _modifiers: int):
        num_dict = {
            arcade.key.NUM_0: "0",
            arcade.key.NUM_1: "1",
            arcade.key.NUM_2: "2",
            arcade.key.NUM_3: "3",
            arcade.key.NUM_4: "4",
            arcade.key.NUM_5: "5",
            arcade.key.NUM_6: "6",
            arcade.key.NUM_7: "7",
            arcade.key.NUM_8: "8",
            arcade.key.NUM_9: "9",
            arcade.key.KEY_0: "0",
            arcade.key.KEY_1: "1",
            arcade.key.KEY_2: "2",
            arcade.key.KEY_3: "3",
            arcade.key.KEY_4: "4",
            arcade.key.KEY_5: "5",
            arcade.key.KEY_6: "6",
            arcade.key.KEY_7: "7",
            arcade.key.KEY_8: "8",
            arcade.key.KEY_9: "9",
        }
        if self.key in num_dict and self.num_flag:
            self.input += num_dict[self.key]

        elif self.key == arcade.key.ENTER:
            resume_game = GameManager.instance.get_game_view()
            try:
                if int(self.input) == self.value1 + self.value2:  # When won
                    # TODO: change to should leave minigame
                    self.input = ""
                    self.num_flag = True
                    
                    #TODO: return to game view
                    self.window.show_view(resume_game)
                    print("You won")

                elif self.tries == 4:  # when no attempt left
                    self.window.show_view(resume_game)
                    print("You lost")
                else:  # when incorrect but attempts still there
                    self.tries += 1
                    self.input = ""
                    self.num_flag = True
            except ValueError:
                self.input = ""
                self.tries += 1

    # To prevent user from entering more than 3 digits
    def update(self, delta_time: float):
        if len(self.input) == 5:
            self.num_flag = False

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(
            C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2, 300, 450, arcade.color.WHITE
        )
        arcade.draw_text(
            f"{self.input}",
            C.SCREEN_WIDTH / 2 - 130,
            C.SCREEN_HEIGHT / 2 + 140,
            arcade.color.BLUE,
            font_size=30,
            anchor_x="left",
            anchor_y="center",
        )
        arcade.draw_text(
            f"{self.value1} + {self.value2} =",
            C.SCREEN_WIDTH / 2 - 130,
            C.SCREEN_HEIGHT / 2 + 200,
            arcade.color.BLACK,
            font_size=15,
            anchor_x="left",
            anchor_y="center",
        )

        self.manager.draw()
