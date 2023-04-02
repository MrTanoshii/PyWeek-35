class StoryManager:
    """Base class for the Story Manager Singleton."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:  # :=
            cls.instance = super(StoryManager, cls).__new__(cls)  # :=
        return cls.instance  # :=

    def __init__(self):
        self.story = [
            "Greetings Human, I need you to guide me through this mission!. Press `Space` to continue.",
            "Some embawassing videos meowight have found their way onto the metabook servers.",
            "The videos are stored somewhere in Face Platforms, Inc's HQ. We need to get them back.",
            "And if things weren't tense enough we have guards patrolling during our little midnight stroll.",
            "They're only human, so turn off the lights with the `E` key at switches and we'll be just fine.",
            "Control me with the `WASD` or arrow keys. The operation begins.",
        ]
        self.current_story_index = -1
        self.special_story = {
            "lights_tutorial": {
                "played": False,
                "story": "You found a light switch. Press `E` to turn interact with it. But be careful, the lights won't be off that long.",
            },
            "safe_tutorial": {
                "played": False,
                "story": "First safe! We'll use the `E` to interact with it and crack it's puzzle!",
            },
            "level_2": {
                "played": False,
                "story": "Meowstirful Stealth tactics partner. It only gets more difficult from here on, so stay on your paws!",
            },
            "level_3": {
                "played": False,
                "story": "Like a shadow on the wall partner! We make a great team as always. Get yourself a cup of milk. You've earned it! ",
            },
            "level_4": {
                "played": False,
                "story": "We're on a hot streak partner. It's only gonna get harder! I'll let you use my scratching post as a reward.",
            },
            "level_5": {
                "played": False,
                "story": "Great job! We've secured the videos and now we can get back to the catnip. I'll be waiting for you at HQ.",
            },
            "safes_tutorial": {
                "played": False,
                "story": "`E` can also be used to interact with safes. So many handy functions for a simple button. I'd say it's `E`xcellent!",
            },
            "safe_0": {
                "played": False,
                "story": "An old floppy disc labelled 'Windows 95 Install Disk #7 / 213'.",
            },
            "safe_1": {
                "played": False,
                "story": "A vinyl record of my favorite jazz titled 'A Cruel Catastrophy' I'll let you listen to it some time!",
            },
            "safe_2": {
                "played": False,
                "story": "An SD card with the movie 'Gangster Cats Come to Paris' this one really got snubbed at the Oscars!",
            },
            "safe_3": {
                "played": False,
                "story": "Oh god it's a memory stick with 62 bitcoin on it. That's about $12 in the bank.",
            },
            "safe_4": {
                "played": False,   # The Safe we are looking for on level 5
                "story": "Hard Drive with all my embarrassing videos. I'm so glad you found it!. Now find your way out.",
            },
            "safe_5": {
                "played": False,  # "empty" safe on level 5
                "story": "Oh, it was just a broken CD. DISAPPOINTED!!! Oh well, there should be another safe somewhere in this room. Keep looking...",
            },
        }

    def next_story(self):
        if self.current_story_index + 1 >= len(self.story):
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

    def play_story(self, story):
        if self.special_story.get(story):
            return self.special_story[story]["story"]
        return None
