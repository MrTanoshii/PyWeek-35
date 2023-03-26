from ursina import *


class Menu(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = Entity(parent=self, enabled=False)
        self.menu.disable()

        Text(text="Shadow Heist", parent=self.menu, origin=(0, 0), position=(0, 2), scale=20)
        btnPlay = Button(text="Play", parent=self.menu, origin=(0, 0), position=(0, 0), scale=(3, 0.66))
        btnPlay.on_click = lambda: self.close()
        btnQuit = Button(text="Quit", parent=self.menu, origin=(0, 0), position=(0, -1), scale=(3, 0.66))
        btnQuit.on_click = lambda: application.quit()

    def open(self):
        self.menu.enable()

    def close(self):
        invoke(setattr, self.menu, 'enabled', False, delay=.5)
