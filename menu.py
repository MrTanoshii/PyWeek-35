from ursina import *


class UI_Button:
    BUTTON_SCALE = (2, 0.5, 1)

    def __init__(self, txt_inp, position, colour, func):
        self.button = Button(
            text=txt_inp, color=colour, scale=UI_Button.BUTTON_SCALE, on_click=func
        )
        self.button.y = position


def resume_func():
    print("Button 1 clicked!")


def options_func():
    print("Button 2 clicked!")


def credits_func():
    print("Button 3 clicked!")


app = Ursina()

window.title = "My Game"
window.fullscreen = False
window.exit_button.visible = False

scene = Entity()

button_lst = [
    UI_Button("Resume", 0.75, color.gray, resume_func),
    UI_Button("Options", 0, color.gray, options_func),
    UI_Button("Credits", -0.75, color.gray, credits_func),
]

for button in button_lst:
    button.button.parent = scene
    button.button.text_entity.scale *= 4.5

app.run()
