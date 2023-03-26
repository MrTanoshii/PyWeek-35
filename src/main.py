from ursina import *
from ursina.prefabs.tilemap import Tilemap

from mainmenu import Menu

app = Ursina(
    vsync=False,
    size=(1280, 720),
    forced_aspect_ratio=16 / 9
)

window.setTitle("Shadow Heist v0.0.1 - PyWeek 35")
window.borderless = False
window.fullscreen = False

# Init menus
main_view = Menu()

game_view = Entity(enabled=False)
tile_map = Tilemap('tilemap_test_level', tileset='test_tileset', tileset_size=(8, 4), parent=game_view)

# add 2d text
Text(text='Press ESC to open the menu', origin=(0, 0), position=(0, 0.4), scale=2, background=True, parent=game_view)


def update():
    if not main_view.menu.enabled:
        game_view.enable()
        camera.orthographic = True
        camera.position = tile_map.tilemap.size / 2
    if held_keys['escape']:
        game_view.disable()
        camera.orthographic = False
        camera.position = (0, 0, -20)
        main_view.open()


main_view.open()

app.run()
