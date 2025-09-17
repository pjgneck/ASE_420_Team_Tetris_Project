class ScoreManager:
    def __init__(self):
        self.score = 0

    def add_points(self, points: int):
        self.score += points

    def should_switch(self) -> bool:
        return self.score != 0 and self.score % 1000 == 0
