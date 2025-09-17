class ScoreManager:
    def __init__(self):
        self.score = 0

    def update(self, lines_cleared):
        self.score += lines_cleared ** 2

    def get_score(self):
        return self.score
