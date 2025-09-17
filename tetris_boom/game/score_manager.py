import os
import json

class ScoreManager:
    def __init__(self, save_path=None):
        if save_path is None:
        # Get the directory where this script is located (game folder)
            script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to tetris_boom folder
            project_root = os.path.dirname(script_dir)
        # Then into assets
            self.save_path = os.path.join(project_root, "assets", "highscore.json")
        else:
            self.save_path = save_path
        self.highscore = 0
        self.score = 0
        self._load_highscore()

    def add_points(self, lines_cleared: int):
        self.score += lines_cleared ** 2

    def get_score(self) -> int:
        return self.score

    def get_highscore(self) -> int:
        return self.highscore

    def reset(self):
        self.score = 0

    def game_over(self):
        """Call this method when the game ends to save the highscore"""
        print(f"Game over! Final score: {self.score}")
        self._save_highscore()
    
    def _load_highscore(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    self.highscore = data.get("highscore", 0)
            except (json.JSONDecodeError, IOError):
                self.highscore = 0

    def _save_highscore(self):
        try:
            if self.score > self.highscore:
                self.highscore = self.score
            
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            
            with open(self.save_path, "w") as f:
                json.dump({"highscore": self.highscore}, f)
            print(f"Highscore saved: {self.highscore}") 
            
        except IOError as error:
            print(f"Error saving highscore: {error}")