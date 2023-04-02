class StoryManager:
    """Base class for the Story Manager Singleton."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:  # :=
            cls.instance = super(StoryManager, cls).__new__(cls)  # :=
        return cls.instance  # :=

    def __init__(self):
        self.story = [
            "Oh, Hello Player, Welcome to the game. Press SPACE to continue.",
            "You have to steal the missing data from the datacenter of our rival company.",
            "The datacenter is located in the basement of the building.",
            "You have to get there undetected.",
            "Good luck, Agent Whiskers.",
            "You need to shut down the lights, so the guards won't see you.",
            "You can do that by pressing the E.",
            "You can also use the E to open the safes.",
            "You can use the WASD keys to move.",
            "Okay then, good luck, Agent Whiskers.",
        ]
        self.current_story_index = -1
        self.special_story = {
            "lights_tutorial": {
                "played": False,
                "story": "You need to shut down the lights, so the guards won't see you. You can do that by pressing the E.",
            },
            "level_2": {
                "played": False,
                "story": "Great job Agent Whiskers. You have successfully passed the first level. But there is still more to do.",
            },
            "level_3": {
                "played": False,
                "story": "Great job Agent Whiskers. You have successfully passed the second level. But there is still more to do.",
            },
            "level_4": {
                "played": False,
                "story": "Great job Agent Whiskers. You have successfully passed the third level. But there is still more to do.",
            },
            "safes_tutorial": {
                "played": False,
                "story": "You can also use the E to open the safes. You can use the WASD keys to move. Okay then, good luck, Agent Whiskers.",
            },
            "safe_0": {
                "played": False,
                "story": 'You found old floppy diskette labeled "Windows 95 - 7/24", Now find exit to the next room.',
            },
            "safe_1": {
                "played": False,
                "story": "You found a vinyl record containing an unreleased album from a Michael Jordan. Go to next level.",
            },
            "safe_2": {
                "played": False,
                "story": "You found an SD card containing Hunter Biden's Laptop backup. Keep searching",
            },
            "safe_3": {
                "played": False,
                "story": "You found a memory stick containing a hundreds of Bitcoins. You’re getting closer, keep looking",
            },
            "safe_4": {
                "played": False,
                "story": "You found Hard Drive with your embarrassing cat video. Now find the exit from the building",
            },
        }

    def next_story(self):
        if self.current_story_index + 1 >= len(self.story):
            print("no more story")
            return None
        self.current_story_index += 1
        return self.story[self.current_story_index]

    def add_story(self, story):
        """
        Add a story to the story list.
        Can be used to add more stories in game loop, for example dialogs.
        """
        self.story.append(story)

    def play_story_if_not_played(self, story):
        if self.special_story.get(story):
            if not self.special_story[story]["played"]:
                self.special_story[story]["played"] = True
                return self.special_story[story]["story"]
        return None
