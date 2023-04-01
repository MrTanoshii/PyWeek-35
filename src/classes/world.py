import arcade
from pytiled_parser.tiled_object import Rectangle, Point
from pathlib import Path

from src.constants import CONSTANTS as C


class World:
    def __init__(self, tile_map: arcade.tilemap.TileMap, map_name: str):
        self.map = tile_map
        self.map_name = map_name

        self.collision = self.map.get_tilemap_layer("collision")
        self.walls: list[Rectangle] = list(filter(lambda x: x.class_ == "wall", self.collision.tiled_objects))

        self.spawns = self.map.get_tilemap_layer("spawner")
        self.player_spawn: list[Rectangle] = list(filter(lambda x: x.class_ == "player", self.spawns.tiled_objects))
        self.guard_spawn: list[Rectangle] = list(filter(lambda x: x.class_ == "guard", self.spawns.tiled_objects))

        self.paths = self.map.get_tilemap_layer("path")
        self.guards_path: list[Rectangle] = list(filter(lambda x: x.class_ == "guard", self.paths.tiled_objects))
        self.guards: list[Rectangle] = list(filter(lambda x: x.class_ == "guard", self.paths.tiled_objects))
        self.lights = list(
            filter(
                lambda x: x.class_ == "light",
                self.map.get_tilemap_layer("lights").tiled_objects,
            )
        )
        self.guard_patrol_points: list[Point] = list(filter(lambda x: x.class_ == "point", self.paths.tiled_objects))

        # Interactables
        self.interactable_layer = self.map.get_tilemap_layer("interactable")
        self.safes: list[Rectangle] = list(filter(lambda x: x.class_ == "safe", self.interactable_layer.tiled_objects))
        self.light_switches: list[Rectangle] = list(filter(lambda x: x.class_ == "light_switch", self.interactable_layer.tiled_objects))

        print(self.light_switches)

    @classmethod
    def load(cls, map_name: str):
        return cls(
            arcade.load_tilemap(Path("src/assets") / "tilemaps" / map_name, scaling=C.WORLD_SCALE),
            map_name=map_name.split(".")[0],  # :=
        )

    @property
    def objects(self):
        return self.collision.tiled_objects

    @property
    def width(self):
        return self.map.width

    @property
    def height(self):
        return self.map.height

    @property
    def tile_size(self):
        return self.map.tile_width

    def tiled_to_screen(self, x: int, y: int) -> tuple[int, int]:
        return x * C.WORLD_SCALE, (self.height * self.tile_size - y) * C.WORLD_SCALE
