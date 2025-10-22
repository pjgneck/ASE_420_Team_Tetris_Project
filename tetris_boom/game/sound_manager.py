import os
import pygame

class SoundManager:
    def __init__(self, sound_path: str = "tetris_boom/assets/sounds"):
        """
        Initializes the sound manager and loads all necessary sounds.

        :param sound_path: The base directory where sound files are stored.
        """
        self.sound_path = sound_path  # Path to the folder with sound files
        self.sounds = {}  # Dictionary to store loaded sounds
        self._load_sounds()

    def _load_sounds(self):
        """
        Loads all required sound files from the given sound directory.
        This method should map sound identifiers to their pygame sound objects.
        """
        # Example placeholder (implement actual loading later)
        # self.sounds["line_clear"] = pygame.mixer.Sound(os.path.join(self.sound_path, "line_clear.wav"))
        self.sounds["game_over"] = pygame.mixer.Sound(os.path.join(self.sound_path, "game_over.mp3"))

    def play(self, sound_name: str):
        """
        Plays a sound effect by its identifier.

        :param sound_name: The key of the sound to play (as defined in self.sounds).
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found.")

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

    def set_volume(self, sound_name: str, volume: float):
        """
        Sets the volume for a specific sound.

        :param sound_name: The key of the sound to adjust.
        :param volume: A float between 0.0 (mute) and 1.0 (full volume).
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)

    def set_master_volume(self, volume: float):
        """
        Sets the master volume for all sounds.

        :param volume: A float between 0.0 and 1.0.
        """
        pygame.mixer.music.set_volume(volume)
