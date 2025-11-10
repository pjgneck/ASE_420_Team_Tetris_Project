import os
import json

from game.sound_manager import SoundManager

class ScoreManager:
    def __init__(self, save_path: str = "tetris_boom/assets/highscore.json"):
        """
        Initializes the score manager, loading the highscore from a file if it exists.

        :param save_path: The file path to save/load the highscore data.
        """
        self.highscore_data = {"name": "", "highscore": 0}  # Highest score ever achieved
        self.score = 0  # Current score of the game session
        self.player_name = ""  # Name of the player with the highscore
        self.save_path = save_path  # Path to the highscore file
        self._load_highscore()  # Load the highscore from file (if exists)

        self.sound_manager = SoundManager()

    def set_player_name(self, name: str):
        """
        Sets the player's name.

        :param name: The name of the player.
        """
        self.player_name = name

    def add_points(self, lines_cleared: int):
        """
        Adds points based on the number of lines cleared. The more lines cleared, the more points added.

        :param lines_cleared: The number of lines cleared by the player in the current move.
        """
        self.score += lines_cleared ** 2  # Example: 1 line = 1 point, 2 lines = 4 points, etc.

        self.sound_manager.play("place_block")

        if lines_cleared > 0:
            if lines_cleared > 10:
                line_clear_sound = "easter_egg"
            elif lines_cleared > 3:
                line_clear_sound = "line_clear_2"
            else:
                line_clear_sound = "line_clear_1"
            
            self.sound_manager.play(line_clear_sound)
        
        if self.score > self.highscore_data["highscore"]:
            self.highscore_data = {
                "name": self.player_name,
                "highscore": self.score
            }
            self._save_highscore()  # Save the new highscore
            self.sound_manager.play("highscore")

    def get_score(self) -> int:
        """
        Gets the current score of the player.

        :return: The current score.
        """
        return self.score

    def get_highscore(self) -> int:
        """
        Gets the highest score ever achieved.

        :return: The highest score.
        """
        return self.highscore_data["highscore"]

    def get_highscore_player(self) -> str:
        """
        Gets the name of the player who achieved the highest score.

        :return: The name of the highscore player.
        """
        return self.highscore_data["name"]

    def reset(self):
        """
        Resets the current score to zero. Highscore remains unchanged.
        """
        self.score = 0

    def _load_highscore(self):
        """
        Loads the highscore from a JSON file, if it exists.

        The highscore will be set to 0 if the file doesn't exist or the data is corrupted.
        """
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    self.highscore_data = {
                        "name": data.get("name", ""),
                        "highscore": data.get("highscore", 0)
                    }
            except (json.JSONDecodeError, IOError) as error:
                print(f"Error loading highscore: {error}")
                self.highscore_data = {"name": "", "highscore": 0}  # Reset to default if there's any error

    def _save_highscore(self):
        """
        Saves the current highscore to a JSON file.
        
        If the directory doesn't exist, it will be created before attempting to write.
        """
        # Ensure the directory exists
        directory = os.path.dirname(self.save_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)  # Create directory if it doesn't exist
            except IOError as error:
                print(f"Error creating directory: {error}")
                return

        # Now save the highscore data
        try:
            with open(self.save_path, "w") as f:
                json.dump(self.highscore_data, f)
        except IOError as error:
            print(f"Error saving highscore: {error}")
