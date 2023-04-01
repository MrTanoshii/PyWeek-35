

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
            "Okay then, good luck, Agent Whiskers."
        ]
        self.current_story_index = -1
        print("story manager initialized")

    def next_story(self):
        if self.current_story_index + 1 >= len(self.story):
            print("no more story")
            return None
        self.current_story_index += 1
        return self.story[self.current_story_index]
