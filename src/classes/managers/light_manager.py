import arcade
from pathlib import Path
from arcade.experimental import Shadertoy

from itertools import chain


class LightManager:
    def __init__(self):
        window_size = arcade.get_window().get_size()
        self.shader: Shadertoy = Shadertoy.create_from_file(
            window_size, Path("src/assets/shaders/lights.glsl")
        )

    def draw_shader(
        self,
        light_sources: list[tuple[int, int, int]],
        walls: list[tuple[int, int, int, int]],
    ):
        lights = list(chain.from_iterable(light_sources)) + [0, 0, 0] * (
            128 - len(light_sources)
        )
        _walls = list(chain.from_iterable(walls)) + [0, 0, 0, 0] * (256 - len(walls))

        self.shader.program["lightSources"] = lights
        self.shader.program["lightCount"] = len(light_sources)
        self.shader.program["obstacles"] = _walls
        self.shader.program["obstaclesCount"] = len(walls)
        self.shader.render()

    def on_resize(self, width: int, height: int):
        self.shader.resize((width, height))
