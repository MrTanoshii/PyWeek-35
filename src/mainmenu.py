from ursina import *


class Menu(Entity):
    MENU_ORIGIN = (0, 0)
    BTN_SCALE = (3, 0.66)
    BTN_COLOR = color.gray

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = Entity(parent=self, enabled=False)
        self.menu.disable()

        Text(
            text="Shadow Heist",
            parent=self.menu,
            origin=Menu.MENU_ORIGIN,
            position=(0, 2),
            scale=20,
        )

        btn_play = Button(
            text="Play",
            parent=self.menu,
            origin=Menu.MENU_ORIGIN,
            position=(0, 1),
            scale=Menu.BTN_SCALE,
            color=Menu.BTN_COLOR,
        )
        btn_play.on_click = lambda: self.close()

        btn_options = Button(
            text="Options",
            parent=self.menu,
            origin=Menu.MENU_ORIGIN,
            position=(0, 0),
            scale=Menu.BTN_SCALE,
            color=Menu.BTN_COLOR,
        )
        btn_options.on_click = lambda: self.options()

        btn_credits = Button(
            text="Credits",
            parent=self.menu,
            origin=Menu.MENU_ORIGIN,
            position=(0, -1),
            scale=Menu.BTN_SCALE,
            color=Menu.BTN_COLOR,
        )
        btn_credits.on_click = lambda: self.credits()

        btn_quit = Button(
            text="Quit",
            parent=self.menu,
            origin=Menu.MENU_ORIGIN,
            position=(0, -2),
            scale=Menu.BTN_SCALE,
            color=Menu.BTN_COLOR,
        )
        btn_quit.on_click = lambda: application.quit()

    def open(self):
        self.menu.enable()

    def close(self):
        invoke(setattr, self.menu, "enabled", False, delay=0.5)

    def options(self):
        pass

    def credits(self):
        pass
