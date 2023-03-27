import arcade
from pathlib import Path
from arcade.experimental import Shadertoy
from arcade.gl import Framebuffer


class LightManager:
    def __init__(self):
        window_size = arcade.get_window().get_size()
        self.shader: Shadertoy = Shadertoy.create_from_file(window_size, Path("assets/shaders/lights.glsl"))
        self.channel0: Framebuffer = self.shader.ctx.framebuffer(
            color_attachments=[self.shader.ctx.texture(window_size, components=4)],
        )
        self.channel1: Framebuffer = self.shader.ctx.framebuffer(
            color_attachments=[self.shader.ctx.texture(window_size, components=4)],
        )

        self.shader.channel_0 = self.channel0.color_attachments[0]
        self.shader.channel_1 = self.channel1.color_attachments[0]

    def on_draw_shadows(self):
        self.channel0.use()
        self.channel0.clear()

    def on_draw(self):
        self.channel1.use()
        self.channel1.clear()

    def on_draw_shader(self, x, y):
        self.shader.program["lightPosition"] = (x, y)
        self.shader.program["lightSize"] = 300
        self.shader.render()

    def on_resize(self, width: int, height: int):
        self.shader.resize((width, height))

