import arcade

from src.constants import CONSTANTS as C
from src.classes.managers.light_manager import LightManager
from src.classes.managers.game_manager import GameManager
from src.classes.wall import Wall
from src.classes.world import World
from src.classes.guard import Guard
from src.classes.hud import HUD


class GameView(arcade.View):
    """Base class for the 'game' view."""

    def __init__(self):
        super().__init__()
        self.scene = None
        self.world = World.load("example.tilemap.json")
        self.guard = None
        self.hud = None
        self.light = LightManager()
        self.physics_engines = []
        self.last_pos = (0, 0)
        self.camera = arcade.Camera(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        self.game_manager = GameManager.instance

        # LAST ??
        self.setup()

    def setup(self):
        """Set up the view."""
        self.scene = arcade.Scene.from_tilemap(self.world.map)

        # Create and append scaled Wall objects from self.world.walls to self.game_manager.walls
        for wall in [
            Wall(
                (wall.coordinates.x + wall.size.width / 2) * C.WORLD_SCALE,
                (self.world.height * self.world.tile_size - wall.coordinates.y - wall.size.height / 2) * C.WORLD_SCALE,
                wall.size.width * C.WORLD_SCALE, wall.size.height * C.WORLD_SCALE
            )
            for wall in self.world.walls
        ]:
            self.game_manager.walls.append(wall)

        # Guard
        for guard in self.world.guard_spawn:
            new_guard: arcade.Sprite = Guard()
            new_guard.center_x = (guard.coordinates.x + guard.size.width / 2) * C.WORLD_SCALE
            new_guard.center_y = (self.world.height * self.world.tile_size - guard.coordinates.y - guard.size.height / 2) * C.WORLD_SCALE
            self.physics_engines.append(arcade.PhysicsEngineSimple(new_guard, self.game_manager.walls))

        self.game_manager.world = self.world

        self.game_manager.world = self.world

        self.game_manager.world = self.world

        self.hud = HUD()

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.ARMY_GREEN)

    def on_draw(self):
        """Draw the view."""
        # Primary camera stuff here:

        self.light.on_draw_shadows()
        # Draw fragments which shouldn't pass the light:
        self.game_manager.walls.draw()

        self.light.on_draw()
        # Draw fragments which can be in the shadow:
        # Put here drawing interactables and guards
        self.game_manager.guards.draw()

        arcade.get_window().use()
        self.clear()
        # TODO: Mihett, should this be kept or removed?
        # self.light.on_draw_shader(C.SCREEN_WIDTH//2, C.SCREEN_HEIGHT//2) # one argument expected

        self.scene.draw()

        self.light.on_draw_shader([
            (
                self.world.tiled_to_screen(light.coordinates.x, light.coordinates.y)[0],
                self.world.tiled_to_screen(light.coordinates.x, light.coordinates.y)[1],  # :=
                light.properties.get("radius", C.DEFAULT_LIGHT_RADIUS)
            )
            for light in self.world.lights
        ])  # [(self.last_pos[0], self.last_pos[1], 300)]

        self.scene.draw()
        self.game_manager.guards.draw()
        self.hud.draw()
        self.camera.use()

    def on_update(self, delta_time: float):
        """Update the view."""
        for engine in self.physics_engines:
            engine.update()
        self.scene.update()
        self.game_manager.guards.on_update(delta_time)

        self.camera.move_to((self.game_manager.player.center_x - C.SCREEN_WIDTH // 2, self.game_manager.player.center_y - C.SCREEN_HEIGHT // 2), 1)

        self.camera.move_to((self.game_manager.player.center_x - C.SCREEN_WIDTH // 2, self.game_manager.player.center_y - C.SCREEN_HEIGHT // 2), 1)

        self.camera.move_to((self.game_manager.player.center_x - C.SCREEN_WIDTH // 2, self.game_manager.player.center_y - C.SCREEN_HEIGHT // 2), 1)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handle mouse press events."""
        pass

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        pass

    def on_resize(self, width: int, height: int):
        self.light.on_resize(width, height)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.last_pos = (x, y)
