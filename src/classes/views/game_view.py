import arcade
from pytiled_parser.tiled_object import Rectangle

from src.classes.entities.light import Light
from src.classes.entities.player import Player
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

    def __init__(self):
        super().__init__()
        self.music_manager = None
        self.scene = None
        self.world = World.load("example.tilemap.json")
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
        self.scene = arcade.Scene.from_tilemap(self.world.map)

        # Create and append scaled Wall objects from self.world.walls to self.game_manager.walls
        for wall in [
            Wall(
                (wall.coordinates.x + wall.size.width / 2) * C.WORLD_SCALE,
                (self.world.height * self.world.tile_size - wall.coordinates.y - wall.size.height / 2) * C.WORLD_SCALE,
                wall.size.width * C.WORLD_SCALE,
                wall.size.height * C.WORLD_SCALE,
            )
            for wall in self.world.walls
        ]:
            self.game_manager.walls.append(wall)

        # Create and append scaled Light objects from self.world.Light to self.game_manager.Light
        for light in self.world.lights:
            new_light: Light = Light(light.properties["radius"])
            new_light.center_x = (light.coordinates.x + light.size.width / 2) * C.WORLD_SCALE
            new_light.center_y = (
                self.world.height * self.world.tile_size - light.coordinates.y - light.size.height / 2
            ) * C.WORLD_SCALE
            self.game_manager.lights.append(new_light)

        # Guard
        for guard in self.world.guard_spawn:
            new_guard: arcade.Sprite = Guard()
            new_guard.center_x = (guard.coordinates.x + guard.size.width / 2) * C.WORLD_SCALE
            new_guard.center_y = (
                self.world.height * self.world.tile_size - guard.coordinates.y - guard.size.height / 2
            ) * C.WORLD_SCALE
            self.physics_engines.append(arcade.PhysicsEngineSimple(new_guard, self.game_manager.walls))
        self.game_manager.world = self.world

        # Let's add the player
        self.player = Player()
        coords = self.game_manager.world.player_spawn[0].coordinates
        self.player.scale = 1
        self.player.center_x = coords.x * C.WORLD_SCALE
        self.player.center_y = (C.SCREEN_HEIGHT - coords.y - 96) * C.WORLD_SCALE
        self.game_manager.set_player(self.player)
        self.hud = HUD()
        self.game_manager.music_manager = music_manager

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
        print(len(lights))
        self.light.draw_shader(
            [
                (
                    self.world.tiled_to_screen(light.coordinates.x, light.coordinates.y)[0] - self.camera.position.x,
                    self.world.tiled_to_screen(light.coordinates.x, light.coordinates.y)[1]
                    - self.camera.position.y,  # :=
                    light.properties.get("radius", C.DEFAULT_LIGHT_RADIUS) * C.WORLD_SCALE,
                )
                for light in lights
            ],
            [self._wall_to_screen_coords(wall) for wall in self.world.walls],
        )

        self.world.map.sprite_lists["collision_tiles"].draw()  # to remove light from collision tiles
        
        for guard in self.game_manager.guards:
            guard.draw()

        self.player.draw()
        if C.DEBUG:
            self.player.draw_hit_box()

        self.hud.draw()
        self.camera.use()

    def on_update(self, delta_time: float):
        """Update the view."""
        GameManager.instance.time += delta_time
        for engine in self.physics_engines:
            engine.update()
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
        if Guard.num_guards_chasing() > 0:
            print('chasing')
            Guard.start_chase()
        else:
            print('not')
            Guard.end_chase()
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        Guard.num_guards_chasing()
        pass

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        pass

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
