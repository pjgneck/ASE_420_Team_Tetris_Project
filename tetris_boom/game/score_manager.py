import os
import json
import copy

from game.sound_manager import SoundManager

class ScoreManager:
    def __init__(self, sound_manager: SoundManager):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)
        save_path = os.path.join(BASE_DIR, "assets", "highscore.json")
        print(save_path)
        
        """
        Initializes the score manager, loading the highscore from a file if it exists.

        :param save_path: The file path to save/load the highscore data.
        """
        self.leaderboard = []  # List of top scores
        self.score = 0  # Current score of the game session
        self.player_name = ""  # Name of the current player
        self.save_path = save_path  # Path to the highscore file
        self._load_leaderboard()  # Load the leaderboard from file (if exists)

        self.sound_manager = sound_manager

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
        
        # Check if current score is higher than the highest score in leaderboard
        highest_score = self.get_highscore()
        if self.score > highest_score:
            self.sound_manager.play("highscore")

    def get_score(self) -> int:
        """
        Gets the current score of the player.

        :return: The current score.
        """
        return self.score

    def reset(self):
        """
        Resets the current score to zero. Highscore remains unchanged.
        """
        self.score = 0

    def get_highscore(self):
        """
        Returns the highest score in the leaderboard
        """
        if self.leaderboard:
            return self.leaderboard[0]["score"]
        return 0
    
    def get_highscore_player(self):
        """
        Returns the highest score player name in the leaderboard
        """
        if self.leaderboard:
            return self.leaderboard[0]["name"]
        return ""

    def _load_leaderboard(self):
        """
        Loads the leaderboard from a JSON file, if it exists.

        The highscore will be set to 0 if the file doesn't exist or the data is corrupted.
        """
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    self.leaderboard = json.load(f)
                # Ensure leaderboard is sorted by score (descending)
                self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
            except:
                self.leaderboard = []
        else:
            self.leaderboard = []

    def _save_leaderboard(self):
        """
        Saves the current leaderboard to a JSON file.
        
        If the directory doesn't exist, it will be created before attempting to write.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def update_leaderboard(self):
        player_name = self.player_name.strip() or "Player"
        player_score = self.get_score()

        # Make a deepcopy of the current leaderboard
        leaderboard = copy.deepcopy(self.leaderboard)

        # Ensure all entries are valid
        leaderboard = [entry for entry in leaderboard if isinstance(entry, dict) and "name" in entry and "score" in entry]

        # Check if player already exists in leaderboard
        existing_player_index = None
        for i, entry in enumerate(leaderboard):
            if entry["name"] == player_name:
                existing_player_index = i
                break

        # If player exists, update their score if current score is higher
        if existing_player_index is not None:
            if player_score > leaderboard[existing_player_index]["score"]:
                leaderboard[existing_player_index]["score"] = player_score
        else:
            # Player doesn't exist, add new entry
            leaderboard.append({"name": player_name, "score": player_score})

        # Sort by score (descending)
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 3
        leaderboard = leaderboard[:3]

        # Save back to file
        self.leaderboard = leaderboard
        self._save_leaderboard()

    def get_leaderboard(self):
        """
        Returns the current top 3 scores as a list of dicts
        """
        return self.leaderboard
