import arcade.gui

from src.constants import CONSTANTS as C


class MainMenuView(arcade.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.levels_box = arcade.gui.UIBoxLayout()  # grid layout
        self.bg = arcade.load_texture("src/assets/art/bg.png")

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=arcade.gui.UILabel(
                    text="Select the level", font_size=18
                ).with_space_around(top=20),
                anchor_x="center_x",
                anchor_y="top",
            )
        )

        for level in range(3):
            level_button = Preview(name="example.tilemap", label="label")

            # level_button.event("on_click")(self.create_on_click(map_name, label))

            self.levels_box.add(level_button)

        self.manager.add(self.levels_box.center_on_screen())

    def create_on_click(self, map_name: str, label: str):
        def level_start_handler(_e):
            self.manager.disable()

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
        hovered = arcade.load_texture(
            f"src/assets/tilemaps/{self.map_name}.png",
        )
        hovered = hovered.create_filled(
            "hovered_preview", (hovered.width, hovered.height), (0, 0, 0, 64)
        )
        super().__init__(
            *args,
            **{
                **kwargs,
                "texture": arcade.load_texture(
                    f"src/assets/tilemaps/{self.map_name}.png",
                ),
                "texture_hovered": hovered,
                "text": self.label,
            },
        )

