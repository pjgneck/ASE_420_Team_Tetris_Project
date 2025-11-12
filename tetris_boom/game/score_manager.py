import os
import json
import copy

class ScoreManager:
    def __init__(self, save_path: str = "tetris_boom/assets/highscore.json"):
        """
        Initializes the score manager, loading the highscore from a file if it exists.

        :param save_path: The file path to save/load the highscore data.
        """
        self.leaderboard = []  # Highest score ever achieved
        self.score = 0  # Current score of the game session
        self.player_name = ""  # Name of the player with the highscore
        self.save_path = save_path  # Path to the highscore file
        self._load_leaderboard()  # Load the highscore from file (if exists)

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
            except:
                self.leaderboard = []

    def _save_leaderboard(self):
        """
        Saves the current highscore to a JSON file.
        
        If the directory doesn't exist, it will be created before attempting to write.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def update_leaderboard(self):
        player_name = self.player_name.strip() or "Player"
        player_score = self.get_score()

        # Load existing leaderboard (already done at init)
        leaderboard = copy.deepcopy(self.leaderboard)

        # Ensure objects are in correct format
        cleaned = []
        for entry in leaderboard:
            if isinstance(entry, dict) and "name" in entry and "score" in entry:
                cleaned.append(entry)
        leaderboard = cleaned

        # Insert new score
        inserted = False
        for i in range(len(leaderboard)):
            if player_score > leaderboard[i]["score"]:
                leaderboard.insert(i, {"name": player_name, "score": player_score})
                inserted = True
                break

        # If score wasn't higher than anything, place at bottom
        if not inserted:
            leaderboard.append({"name": player_name, "score": player_score})

        # Keep top 3 only
        leaderboard = leaderboard[:3]

        # Save back to file
        self.leaderboard = leaderboard
        self._save_leaderboard()

    def get_leaderboard(self):
        """
        Returns the current top 3 scores as a list of dicts
        """
        return self.leaderboard