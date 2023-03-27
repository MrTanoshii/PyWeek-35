import arcade
from pytiled_parser.tiled_object import Rectangle
from pathlib import Path

from constants import CONSTANTS as C


class World:
    def __init__(self, tile_map: arcade.tilemap.TileMap, map_name: str):
        self.map = tile_map
        self.map_name = map_name
        self.collision = self.map.get_tilemap_layer("collision")
        self.walls: list[Rectangle] = list(filter(lambda x: x.class_ == "wall", self.objects))

    @classmethod
    def load(cls, map_name: str):
        return cls(
            arcade.load_tilemap(Path("assets") / "tilemaps" / map_name, scaling=C.WORLD_SCALE),
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

