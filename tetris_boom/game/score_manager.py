import os
import json

class ScoreManager:
    def __init__(self, save_path="tetris_boom/assets/highscore.json"):
        self.highscore = 0
        self.score = 0
        self.save_path = save_path
        self._load_highscore()

    def add_points(self, lines_cleared: int):
        self.score += lines_cleared ** 2
        if self.score > self.highscore:
            self.highscore = self.score
            self._save_highscore()

    def get_score(self) -> int:
        return self.score

    def get_highscore(self) -> int:
        return self.highscore

    def reset(self):
        self.score = 0

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
            with open(self.save_path, "w") as f:
                json.dump({"highscore": self.highscore}, f)
        except IOError as error:
            print(error)
