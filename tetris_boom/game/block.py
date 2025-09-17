import random

COLORS = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

FIGURES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(FIGURES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def get_image(self):
        return FIGURES[self.type][self.rotation]

    def get_color(self):
        return COLORS[self.color]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

    def undo_rotate(self):
        self.rotation = (self.rotation - 1) % len(FIGURES[self.type])

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
