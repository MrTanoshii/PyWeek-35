import arcade.gui

from src.constants import CONSTANTS as C


class MainMenuView(arcade.View):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.levels_box1 = arcade.gui.UIBoxLayout(vertical=False)  # grid layout
        self.levels_box2 = arcade.gui.UIBoxLayout(vertical=False)  # grid layout
        self.levels_label_box1 = arcade.gui.UIBoxLayout(vertical=False)  # grid layout
        self.levels_label_box2 = arcade.gui.UIBoxLayout(vertical=False)  # grid layout
        self.bg = arcade.load_texture("src/assets/art/bg.png")

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=arcade.gui.UILabel(
                    text="Select the Level", font_size=32
                ).with_space_around(top=48),
                anchor_x="center_x",
                anchor_y="top",
            )
        )

        for level in range(1, 4):
            level_button = Preview(name=f"level_{level}", label=f"Level {level}")
            level_label = arcade.gui.UILabel(text=f"Level {level}", font_size=24, color=arcade.color.WHITE)

            level_button.event("on_click")(self.create_on_click(level))

            self.levels_box1.add(level_button.with_space_around(0, 50, 125, 50))

            self.levels_label_box1.add(level_label.with_space_around(0, 150, 400, 150))

        for level in range(4, 6):
            level_button = Preview(name=f"level_{level}", label=f"Level {level}")
            level_label = arcade.gui.UILabel(text=f"Level {level}", font_size=24, color=arcade.color.WHITE)

            level_button.event("on_click")(self.create_on_click(level))

            self.levels_box2.add(level_button.with_space_around(425, 50, 0, 50))

            self.levels_label_box2.add(level_label.with_space_around(150, 150, 0, 150))

        self.manager.add(self.levels_box1.center_on_screen())
        self.manager.add(self.levels_box2.center_on_screen())
        self.manager.add(self.levels_label_box1.center_on_screen())
        self.manager.add(self.levels_label_box2.center_on_screen())

    def create_on_click(self, level: int):
        def level_start_handler(_e):
            self.manager.disable()
            self.game.start_level(level)

        return level_start_handler

    def on_update(self, delta_time: float):
        self.manager.on_update(delta_time)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.manager.on_mouse_press(x, y, button, modifiers)

    def on_draw(self):
        self.bg.draw_sized(
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            C.SCREEN_WIDTH,
            C.SCREEN_HEIGHT,
        )
        self.manager.draw()


class Preview(arcade.gui.UITextureButton):
    def __init__(self, name, label, *args, **kwargs):
        self.map_name = name
        self.label = label
        texture = arcade.load_texture(f"src/assets/tilemaps/{self.map_name}.png")
        hovered = arcade.load_texture(f"src/assets/tilemaps/{self.map_name}.png")
        hovered = hovered.create_filled(
            "hovered_preview", (hovered.width, hovered.height), (0, 0, 0, 64)
        )
        super().__init__(*args,
                         **{
                             **kwargs,
                             "texture": texture,
                             "style": {
                                    "font_size": 24,
                                    "font_color": arcade.color.BLACK,
                             }
                         }
                         )  # :=
        self.scale(0.5)
        self.texture_hovered = hovered
        # self.text = self.label
        self.style["font_color"] = arcade.color.BLACK
