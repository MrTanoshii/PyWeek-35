import arcade
import arcade.gui as GUI

from src.constants import CONSTANTS as C

class SafeMini(arcade.View):
    """Safe Mini Game"""
    
    SWITCH_SIZE = 1.0

    def __init__(self):
        button_width = 50
        button_height = 35

        super().__init__()
        arcade.set_background_color(C.BACKGROUND_COLOR)
        
        self.manager = GUI.UIManager()
        self.manager.enable()
        
        self.v_box = GUI.UIBoxLayout()

        # num1_button = GUI.UIFlatButton(text="1", x= C.SCREEN_WIDTH / 4,y= C.SCREEN_HEIGHT / 4, width=button_width, height=button_height)
        num1_button = GUI.UIFlatButton(text="1", center_x= C.SCREEN_WIDTH / 4, center_y= C.SCREEN_HEIGHT / 4, width=button_width, height=button_height)

        self.v_box.add(num1_button)
        
        # Creating buttons
        self.manager.add(
            GUI.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(C.SCREEN_WIDTH / 2, C.SCREEN_HEIGHT / 2, 300, 500, arcade.color.WHITE)
        self.manager.draw()
    #     self.calculator = arcade.Sprite(
    #         "src/assets/art/safe/calculator.png",
    #         SafeMini.SWITCH_SIZE,
    #     )
    #     self.calculator.center_x = C.SCREEN_WIDTH / 2
    #     self.calculator.center_y = C.SCREEN_HEIGHT / 2
        
    #     self.calculator.draw()

    # def on_draw(self):
    #     self.clear()
    #     arcade.draw_lrtb_rectangle_filled(50.0, 50.0, 25.0, 25.0, arcade.color.WHITE)