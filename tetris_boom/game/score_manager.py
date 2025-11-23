import os
import json
import copy
import sys

from game.sound_manager import SoundManager
from game.resource_path import resource_path

class ScoreManager:
    def __init__(self, sound_manager: SoundManager):
        """
        Initializes the score manager, loading the highscore from a file if it exists.

        :param sound_manager: The sound manager instance for playing sounds.
        """
        if getattr(sys, 'frozen', False):
            home_dir = os.path.expanduser("~")
            save_dir = os.path.join(home_dir, ".tetris_boom")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, "highscore.json")
        else:
            save_path = resource_path("assets/highscore.json")
        self.leaderboard = []
        self.score = 0
        self.player_name = ""
        self.save_path = save_path
        self._load_leaderboard()

        self.sound_manager = sound_manager
        self.initial_highscore = self.get_highscore()
        self.highscore_sound_played = False

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
        self.score += lines_cleared ** 2

        self.sound_manager.play("place_block")

        if lines_cleared > 0:
            if lines_cleared > 10:
                line_clear_sound = "easter_egg"
            elif lines_cleared > 3:
                line_clear_sound = "line_clear_2"
            else:
                line_clear_sound = "line_clear_1"
            
            self.sound_manager.play(line_clear_sound)
        
        if (self.initial_highscore > 0 and 
            not self.highscore_sound_played and 
            self.score > self.initial_highscore):
            self.sound_manager.play("highscore")
            self.highscore_sound_played = True

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
        self.initial_highscore = self.get_highscore()
        self.highscore_sound_played = False

    def get_highscore(self):
        """
        Returns the highest score in the leaderboard (excluding scores of 0)
        """
        if self.leaderboard:
            valid_scores = [entry["score"] for entry in self.leaderboard if entry.get("score", 0) > 0]
            if valid_scores:
                return max(valid_scores)
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
        Scores of 0 are filtered out.
        """
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    self.leaderboard = json.load(f)
                self.leaderboard = [
                    entry for entry in self.leaderboard 
                    if isinstance(entry, dict) and "name" in entry and "score" in entry and entry["score"] > 0
                ]
                self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
            except (json.JSONDecodeError, IOError, OSError, KeyError, ValueError):
                self.leaderboard = []
        else:
            self.leaderboard = []

    def _save_leaderboard(self):
        """
        Saves the current leaderboard to a JSON file.
        
        If the directory doesn't exist, it will be created before attempting to write.
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def update_leaderboard(self):
        player_name = self.player_name.strip() or "Player"
        player_score = self.get_score()

        if player_score == 0:
            return

        leaderboard = copy.deepcopy(self.leaderboard)

        leaderboard = [
            entry for entry in leaderboard 
            if isinstance(entry, dict) and "name" in entry and "score" in entry and entry["score"] > 0
        ]

        existing_player_index = None
        for i, entry in enumerate(leaderboard):
            if entry["name"] == player_name:
                existing_player_index = i
                break

        if existing_player_index is not None:
            if player_score > leaderboard[existing_player_index]["score"]:
                leaderboard[existing_player_index]["score"] = player_score
        else:
            leaderboard.append({"name": player_name, "score": player_score})

        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        leaderboard = leaderboard[:3]

        self.leaderboard = leaderboard
        self._save_leaderboard()

    def get_leaderboard(self):
        """
        Returns the current top 3 scores as a list of dicts
        """
        return self.leaderboard
