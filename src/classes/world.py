import arcade
from pytiled_parser.tiled_object import Rectangle, Point
from pathlib import Path

from itertools import starmap
from functools import lru_cache
from operator import itemgetter
import numpy as np

from src.constants import CONSTANTS as C


class World:
    def __init__(self, tile_map: arcade.tilemap.TileMap, map_name: str):
        self.map = tile_map
        self.map_name = map_name

        self.collision = self.map.get_tilemap_layer("collision")
        self.walls: list[Rectangle] = list(
            filter(lambda x: x.class_ == "wall", self.collision.tiled_objects)
        )

        self.grid = np.full((int(self.map.width), int(self.map.height)), 0)
        # print(self.grid.shape)
        for wall in self.walls:
            x, y = self.screen_to_tile(
                *map(
                    int,
                    self.tiled_to_screen(
                        int(wall.coordinates.x), int(wall.coordinates.y)
                    ),
                )
            )
            for i in range(int(wall.size.width) // int(self.map.tile_width)):
                for j in range(int(wall.size.height) // int(self.map.tile_height)):
                    try:
                        self.grid[x + i, int(self.map.height) - (y - j)] = 1
                    except IndexError:
                        # print(x + i, y - j)
                        pass
        # print(self.grid.T)

        self.spawns = self.map.get_tilemap_layer("spawner")
        self.player_spawn: list[Rectangle] = list(
            filter(lambda x: x.class_ == "player", self.spawns.tiled_objects)
        )
        self.guard_spawn: list[Rectangle] = list(
            filter(lambda x: x.class_ == "guard", self.spawns.tiled_objects)
        )

        self.servers = self.map.get_tilemap_layer("server")

        self.paths = self.map.get_tilemap_layer("path")
        self.guards_path: list[Rectangle] = list(
            filter(lambda x: x.class_ == "guard", self.paths.tiled_objects)
        )
        self.guards: list[Rectangle] = list(
            filter(lambda x: x.class_ == "guard", self.paths.tiled_objects)
        )
        self.lights = list(
            filter(
                lambda x: x.class_ == "light",
                self.map.get_tilemap_layer("lights").tiled_objects,
            )
        )
        self.guard_patrol_points: list[Point] = list(
            filter(lambda x: x.class_ == "point", self.paths.tiled_objects)
        )

        # Interactables
        self.interactable_layer = self.map.get_tilemap_layer("interactable")
        self.safes: list[Rectangle] = list(
            filter(lambda x: x.class_ == "safe", self.interactable_layer.tiled_objects)
        )
        self.light_switches: list[Rectangle] = list(
            filter(
                lambda x: x.class_ == "light_switch",
                self.interactable_layer.tiled_objects,
            )
        )

        # print(self.light_switches)
        # print(self.safes)

    @classmethod
    def load(cls, map_name: str):
        return cls(
            arcade.load_tilemap(
                Path("src/assets") / "tilemaps" / map_name, scaling=C.WORLD_SCALE
            ),
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

    def screen_to_tile(self, x: int, y: int) -> tuple[int, int]:
        """
        :param x: absolute x coordinate
        :param y: absolute y coordinate
        :return:
        """

        return int(x / C.WORLD_SCALE) // int(self.map.tile_width), int(
            y / C.WORLD_SCALE
        ) // int(self.map.tile_height)

    def tile_to_screen(self, tile_x: int, tile_y: int) -> tuple[int, int]:
        return int(
            (tile_x * self.map.tile_width + self.map.tile_width // 2) * C.WORLD_SCALE
        ), int(
            (tile_y * self.map.tile_height + self.map.tile_height // 2) * C.WORLD_SCALE
        )

    @lru_cache()
    def pathfinding(
        self, start: tuple[int, int], destination: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """
        A* algorithm realization
        Uses manhattan distance as heuristics

        :param start: tuple of absolute coordinates of start position
        :param destination: tuple of absolute coordinates of destination position
        :return: list of absolute coordinates or None if path not found
        """

        start_tile = self.screen_to_tile(*start)
        destination_tile = self.screen_to_tile(*destination)
        # print(self.grid[destination_tile])
        # print(destination_tile)

        lengths = np.full((int(self.map.width), int(self.map.height)), -1)
        lengths[start_tile] = 0
        path = [start_tile]

        heap = [(0, path)]
        result_path = []

        while heap:
            current_path = min(heap, key=itemgetter(0))
            heap.remove(current_path)
            current_path = current_path[1]

            current_position = current_path[-1]
            if current_position == destination_tile:
                result_path = current_path
                break

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (int(i) ^ int(j)):
                        continue
                    x, y = current_position[0] + i, current_position[1] + j
                    updated_path = current_path.copy()
                    updated_path.append((x, y))

                    if x < 0 or x >= self.map.width or y < 0 or y >= self.map.height:
                        continue

                    if lengths[x, y] != -1:
                        continue

                    if self.grid[x, y]:
                        continue

                    lengths[x, y] = lengths[current_position] + 1
                    total_cost = lengths[current_position] + (
                        abs(x - destination_tile[0]) + abs(y - destination_tile[1])
                    )

                    heap.append((total_cost, updated_path.copy()))

        if not result_path:
            return None

        return list(starmap(self.tile_to_screen, result_path))
