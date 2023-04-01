import os

import arcade


class MusicManager:
    def __init__(self):
        self.music = None
        self.music_list = {}
        self.music_index = 0
        self.current = None

        self.path = f"src/assets/music/"

        self.setup()

    def setup(self):
        for idx, asset in enumerate(os.listdir(self.path)):
            music = arcade.Sound(f"{self.path}/{asset}")
            self.music_list[asset.split(".")[0]] = music

    def play(self, name):
        self.stop()
        self.music = self.music_list[name]
        self.current = self.current = self.music.play(0.5)

    def stop(self):
        if self.music:
            self.music.stop(self.current)
    def play_outro(self):
        self.music = self.music_list["outro"]
        self.current = self.music.play(0.5)

    def play_main(self):
        self.music = self.music_list["main"]
        self.current = self.music.play(0.5)

    def play_chase(self):
        self.stop()
        self.music = self.music_list["chase"]
        self.current = self.music.play(0.5)

    def end_chase(self):
        self.stop()
        self.music = self.music_list["main"]
        self.current = self.music.play()

    def play_outro(self):
        self.stop()
        self.music = self.music_list["outro"]
        self.current = self.music.play(0.5)

    def stop_outro(self):
        self.stop()

    def get_current_key(self):
        for key, value in self.music_list.items():
            if value == self.music:
                return key
