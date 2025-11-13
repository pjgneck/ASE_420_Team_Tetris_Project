import os
import pygame

class SoundManager:


    def __init__(self):
        """
        Initializes the sound manager and loads all necessary sounds.
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sound_path = os.path.join(BASE_DIR, "assets", "sounds")
        self.sounds = {}  # Dictionary to store loaded sounds

        self._load_sounds()
        self._set_default_volumes()

    
    def load(self, name):
        return pygame.mixer.Sound(os.path.join(self.sound_path, f"{name}.ogg"))

    def _load_sounds(self):
        """
        Loads all required sound files from the given sound directory.
        """
        self.sounds = {
            "music_1_loop": pygame.mixer.Sound(os.path.join(self.sound_path, "music_1_loop.ogg")),
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
        loops = -1 if loop else 0
        
        # Special handling for music to ensure it doesn't duplicate
        if sound_name in ["music_1", "music_1_loop"] and loop:
            # Stop any currently playing music before starting new loop
            self._stop_all_music()
            sound.play(loops=-1)
        else:
            # Let pygame automatically handle channel allocation for all other sounds
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

    def _stop_all_music(self):
        """
        Stops all music tracks to prevent duplication.
        """
        for name in ["music_1", "music_1_loop"]:
            if name in self.sounds:
                self.sounds[name].stop()

    def _set_default_volumes(self):
        """Set default volumes for different sound types."""
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
