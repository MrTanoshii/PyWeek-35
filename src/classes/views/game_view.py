from random import randint
import arcade
from pytiled_parser.tiled_object import Rectangle

from src.classes.entities.light import Light
from src.classes.entities.player import Player
from src.classes.entities.server_light import ServerLight
from src.classes.interactables.light_switch import LightSwitch
from src.classes.interactables.safe import Safe
from src.classes.managers.music_manager import MusicManager
from src.constants import CONSTANTS as C
from src.classes.managers.light_manager import LightManager
from src.classes.managers.game_manager import GameManager
from src.classes.wall import Wall
from src.classes.world import World
from src.classes.entities.guard import Guard
from src.classes.hud import HUD


class GameView(arcade.View):
    """Base class for the 'game' view."""

    def __init__(self, level):
        super().__init__()
        self.level = level
        self.music_manager = None
        self.scene = None
        self.world = None
        self.guard = None
        self.hud = None
        self.light = LightManager()
        self.physics_engines = []
        self.last_pos = (0, 0)
        self.camera = arcade.Camera(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        self.game_manager = GameManager.instance
        self.player = None

        # LAST ??
        self.setup()

    def setup(self, music_manager: MusicManager = None):
        """Set up the view."""
        self.world = World.load(f"level_{self.level - 1}.tilemap.json")
        self.scene = arcade.Scene.from_tilemap(self.world.map)

        # Create and append scaled Wall objects from self.world.walls to self.game_manager.walls
        for wall in [
            Wall(
                (wall.coordinates.x + wall.size.width / 2) * C.WORLD_SCALE,
                (
                    self.world.height * self.world.tile_size
                    - wall.coordinates.y
                    - wall.size.height / 2
                )
                * C.WORLD_SCALE,
                wall.size.width * C.WORLD_SCALE,
                wall.size.height * C.WORLD_SCALE,
            )
            for wall in self.world.walls
        ]:
            self.game_manager.walls.append(wall)

        # Create and append scaled Light objects from self.world.Light to self.game_manager.Light
        for light in self.world.lights:
            new_light: Light = Light(light.properties["radius"])
            new_light.center_x = (
                light.coordinates.x + light.size.width / 2
            ) * C.WORLD_SCALE
            new_light.center_y = (
                self.world.height * self.world.tile_size
                - light.coordinates.y
                - light.size.height / 2
            ) * C.WORLD_SCALE
            self.game_manager.lights.append(new_light)

        # Guard
        for guard in self.world.guard_spawn:
            new_guard: arcade.Sprite = Guard()
            new_guard.center_x = (
                guard.coordinates.x + guard.size.width / 2
            ) * C.WORLD_SCALE
            new_guard.center_y = (
                self.world.height * self.world.tile_size
                - guard.coordinates.y
                - guard.size.height / 2
            ) * C.WORLD_SCALE

        # Light Switch
        for switch in self.world.light_switches:
            light_switch = LightSwitch()
            light_switch.center_x = (
                switch.coordinates.x + switch.size.width / 2
            ) * C.WORLD_SCALE
            light_switch.center_y = (
                self.world.height * self.world.tile_size
                - switch.coordinates.y
                - switch.size.height / 2
            ) * C.WORLD_SCALE
            self.game_manager.light_switches.append(light_switch)
            for light in self.game_manager.lights:
                light_switch.lights.append(light)

        # Safe
        for safe in self.world.safes:
            safe_obj = Safe(safe.properties["index"])
            safe_obj.center_x = (
                safe.coordinates.x + safe.size.width / 2
            ) * C.WORLD_SCALE
            safe_obj.center_y = (
                self.world.height * self.world.tile_size
                - safe.coordinates.y
                - safe.size.height / 2
            ) * C.WORLD_SCALE
            self.game_manager.safes.append(safe_obj)
        ServerLight.servers.clear()

        self.game_manager.total_safes_in_level = len(self.game_manager.safes)

        for server in self.world.servers.tiled_objects:
            for _ in range(randint(1, 12)):
                serverlight = ServerLight()
                serverlight.center_x = (
                    server.coordinates.x + server.size.width / 2
                ) * C.WORLD_SCALE
                serverlight.center_y = (
                    self.world.height * self.world.tile_size
                    - server.coordinates.y
                    - server.size.height / 2
                ) * C.WORLD_SCALE

        self.game_manager.world = self.world

        # Let's add the player
        self.player = Player()
        self.player.scale = 0.3 * C.WORLD_SCALE
        coords = self.game_manager.world.player_spawn[0].coordinates
        self.player.scale = .2 * C.WORLD_SCALE
        self.player.center_x = coords.x * C.WORLD_SCALE + self.player.width / 2
        self.player.center_y = (self.world.height * self.world.tile_size - coords.y) * C.WORLD_SCALE - self.player.height / 2
        self.game_manager.set_player(self.player)
        self.hud = HUD()
        self.game_manager.hud = self.hud
        self.game_manager.music_manager = music_manager

        # Level specific story
        custom_story = self.game_manager.story_manager.play_story_if_not_played(f"level_{self.level}")
        if custom_story:
            self.hud.set_story_line(custom_story)

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.ARMY_GREEN)

    def on_draw(self):
        """Draw the view."""
        # Primary camera stuff here:

        arcade.get_window().use()
        self.clear()

        # Draw fragments which can be in the shadow:
        # Put here drawing interactables and guards
        self.scene.draw()
        self.game_manager.guards.draw()

        lights = []
        for idx, light in enumerate(self.game_manager.lights):
            light.draw()
            if light.enabled:
                lights.append(self.world.lights[idx])
        self.light.draw_shader(
            [
                (
                    self.world.tiled_to_screen(
                        light.coordinates.x, light.coordinates.y
                    )[0]
                    - self.camera.position.x,
                    self.world.tiled_to_screen(
                        light.coordinates.x, light.coordinates.y
                    )[1]
                    - self.camera.position.y,  # :=
                    light.properties.get("radius", C.DEFAULT_LIGHT_RADIUS)
                    * C.WORLD_SCALE,
                )
                for light in lights
            ],
            [self._wall_to_screen_coords(wall) for wall in self.world.walls],
        )

        self.world.map.sprite_lists[
            "collision_tiles"
        ].draw()  # to remove light from collision tiles

        self.game_manager.safes.draw()

        for guard in self.game_manager.guards:
            guard.draw()

        self.player.draw()
        if C.DEBUG:
            self.player.draw_hit_box()
            self.player.player_laser.draw_hit_box()
        for lightswitch in GameManager.instance.light_switches:
            lightswitch.draw()
            lightswitch.draw_hit_box()
        for serverlight in ServerLight.servers:
            serverlight.draw()
        self.hud.draw()
        self.camera.use()

    def on_update(self, delta_time: float):
        """Update the view."""
        # for engine in self.physics_engines:
        #     engine.update()
        if C.DEBUG and 1 / delta_time < 50:
            print(f"LOW FPS: {int(1 / delta_time)}")
        GameManager.instance.time += delta_time
        self.scene.update()
        self.player.on_update(delta_time=delta_time)
        self.game_manager.guards.on_update(delta_time)
        self.game_manager.lights.on_update(delta_time)
        self.camera.move_to(
            (
                self.game_manager.player.center_x - C.SCREEN_WIDTH // 2,
                self.game_manager.player.center_y - C.SCREEN_HEIGHT // 2,
            ),
            1,
        )
        self.hud.on_update(delta_time)

        for server in ServerLight.servers:
            server.on_update(delta_time)

        self.game_manager.light_switches.on_update(delta_time)
        self.game_manager.safes.on_update(delta_time)

        if Guard.num_guards_chasing() > 0:
            Guard.start_chase()
        else:
            Guard.end_chase()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        Guard.num_guards_chasing()
        pass

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        pass

    def on_key_release(self, key, modifiers):
        """Handle key press events."""
        GameManager.instance.save_game_view(self)
        for light_switch in self.game_manager.light_switches:
            light_switch.on_key_release(key, modifiers)

        for safe in self.game_manager.safes:
            safe.on_key_release(key, modifiers)

        self.hud.on_key_release(key, modifiers)

    def on_resize(self, width: int, height: int):
        self.light.on_resize(width, height)

    def _wall_to_screen_coords(self, wall: Rectangle) -> tuple[int, int, int, int]:
        x_1, y_1 = self.world.tiled_to_screen(wall.coordinates.x, wall.coordinates.y)
        x_1, y_1 = [x_1 - self.camera.position.x, y_1 - self.camera.position.y]
        x_2, y_2 = (
            x_1 + wall.size.width * C.WORLD_SCALE,
            y_1 - wall.size.height * C.WORLD_SCALE,
        )

        return x_1, y_1, x_2, y_2
