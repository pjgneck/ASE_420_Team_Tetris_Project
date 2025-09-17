from game.block_data import FIGURES, COLORS
import random

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(FIGURES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(FIGURES[self.type])

    def undo_rotate(self):
        self.rotation = (self.rotation - 1) % len(FIGURES[self.type])
    
    def get_image(self):
        return FIGURES[self.type][self.rotation]

    def get_color(self):
        return COLORS[self.color]
