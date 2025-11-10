import os
import pygame

class SoundManager:
    def __init__(self, sound_path: str = None):
        base_dir = os.path.dirname(__file__)
        if sound_path is None:
            # Proper cross-platform path
            self.sound_path = os.path.join(base_dir, "..", "assets", "sounds")
        else:
            self.sound_path = sound_path

        """
        Initializes the sound manager and loads all necessary sounds.

        :param sound_path: The base directory where sound files are stored.
        """
        self.sounds = {}  # Dictionary to store loaded sounds
        pygame.mixer.set_num_channels(16)  # allow many concurrent sounds

        # Create dedicated channels for different sound types
        self.channels = {
            "music": pygame.mixer.Channel(0),
            "effects_1": pygame.mixer.Channel(1),
            "effects_2": pygame.mixer.Channel(2),
            "effects_3": pygame.mixer.Channel(3),
            "alerts": pygame.mixer.Channel(4),
            "misc": pygame.mixer.Channel(5)
        }

        self._load_sounds()
        self._assign_channels()
        self._set_default_volumes()

    def _load_sounds(self):
        """
        Loads all required sound files from the given sound directory.
        This method should map sound identifiers to their pygame sound objects.
        """
        def load(name):
            return pygame.mixer.Sound(os.path.join(self.sound_path, f"{name}.ogg"))

        self.sounds = {
            "game_start": load("game_start"),
            "game_over": load("game_over"),
            "music_1": load("music_1"),
            "rotate_block": load("rotate_block"),
            "place_block": load("place_block"),
            "line_clear_1": load("line_clear_1"),
            "line_clear_2": load("line_clear_2"),
            "switch_modes": load("switch_modes"),
            "highscore": load("highscore"),
            "easter_egg": load("easter_egg"),
        }

    def play(self, sound_name: str, loop=False):
        """
        Plays a sound effect by its identifier.

        :param sound_name: The key of the sound to play (as defined in self.sounds).
        """
        if sound_name not in self.sounds:
            print(f"[SoundManager] Sound '{sound_name}' not found.")
            return

        sound = self.sounds[sound_name]
        category = self.channel_map.get(sound_name, "effects")
        channel = self.channels.get(category)
        loops = -1 if loop else 0

        if channel:
            if loop and channel.get_busy():
                return
            channel.play(sound, loops=loops)
        else:
            sound.play(loops=loops)

    def stop(self, sound_name: str):
        """
        Stops a specific sound if it is currently playing.

        :param sound_name: The key of the sound to stop.
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def stop_all(self):
        """
        Stops all currently playing sounds.
        """
        pygame.mixer.stop()

    def _assign_channels(self):
        """
        Assign each sound to an appropriate channel category.
        This keeps 'play("sound")' usage simple and lag-free.
        """
        self.channel_map  = {
            "game_start": "alerts",
            "game_over": "alerts",
            "music_1": "music",
            "rotate_block": "effects_1",
            "place_block": "effects_2",
            "line_clear_1": "effects_3",
            "line_clear_2": "effects_3",
            "easter_egg": "effects_3",
            "switch_modes": "alerts",
            "highscore": "alerts"
        }

    def _set_default_volumes(self):
        """Set category-based default volumes."""
        for sfx_name, sound in self.sounds.items():
            if "music" in sfx_name:
                sound.set_volume(0.4)
            elif "line_clear" in sfx_name:
                sound.set_volume(0.6)
            elif "game_over" in sfx_name or "highscore" in sfx_name:
                sound.set_volume(0.8)
            else:
                sound.set_volume(0.5)

    def set_master_volume(self, volume: float):
        """
        Sets the master volume for all sounds.

        :param volume: A float between 0.0 and 1.0.
        """
        pygame.mixer.music.set_volume(volume)
